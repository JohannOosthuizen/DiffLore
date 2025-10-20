import os
import time
import difflib
import requests
import yaml
import argparse
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from glob import fnmatch
import ast  # For dependency parsing

class DocHandler(FileSystemEventHandler):
    def __init__(self, config):
        self.config = config
        self.last_processed = {}  # For debouncing per file

    def on_modified(self, event):
        if event.is_directory:
            return
        if any(fnmatch.fnmatch(event.src_path, pattern) for pattern in self.config['file_patterns']):
            now = time.time()
            if event.src_path in self.last_processed and now - self.last_processed[event.src_path] < 5:  # 5s debounce
                return
            self.last_processed[event.src_path] = now
            print(f"Detected change: {event.src_path}")
            self.generate_and_diff(event.src_path)

    def extract_dependencies(self, code: str, code_path: str) -> str:
        """Parse code for imports and basic interdependencies."""
        try:
            tree = ast.parse(code)
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imports.extend([alias.name for alias in node.names])
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ''
                    imports.append(f"{module} (imports: {', '.join(alias.name for alias in node.names)})")
            
            # Stub for reverse deps; expand as needed
            reverse_deps = []
            
            return f"Detected dependencies: {', '.join(imports)}. Reverse dependencies: {', '.join(reverse_deps)}."
        except SyntaxError:
            return "Unable to parse dependencies (non-Python or syntax error)."

    def generate_docs(self, code_path: str) -> str:
        # Retry opening the file in case it's locked during copy
        retries = 3
        delay = 0.5
        for attempt in range(retries):
            try:
                with open(code_path, 'r') as f:
                    code = f.read()
                break
            except PermissionError:
                if attempt < retries - 1:
                    time.sleep(delay)
                else:
                    raise
        
        dep_hint = self.extract_dependencies(code, code_path)
        prompt = self.config['prompt_template'].format(code=code) + f"\n\nDependency Hint: {dep_hint}"
        
        provider = self.config['llm']['provider']
        api_key = self.config['llm'].get('api_key', '')  # Optional for local
        endpoint = self.config['llm'].get('endpoint', 'chat')  # 'chat' or 'completion'
        
        if provider == 'grok':
            url = "https://api.x.ai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        elif provider == 'openai':
            url = "https://api.openai.com/v1/chat/completions"
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        elif provider == 'anthropic':
            url = "https://api.anthropic.com/v1/messages"
            headers = {"x-api-key": api_key, "anthropic-version": "2023-06-01", "Content-Type": "application/json"}
        elif provider == 'ollama':
            base_url = self.config['llm'].get('url', "http://localhost:11434")
            url = f"{base_url}/v1/{'chat/completions' if endpoint == 'chat' else 'completions'}"
            headers = {"Content-Type": "application/json"}  # No auth needed for local
        elif provider == 'lmstudio':
            base_url = self.config['llm'].get('url', "http://localhost:1234")
            url = f"{base_url}/v1/{'chat/completions' if endpoint == 'chat' else 'completions'}"
            headers = {"Authorization": f"Bearer lm-studio", "Content-Type": "application/json"}  # Dummy key for LM Studio
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
        
        if endpoint == 'chat':
            payload = {
                "model": self.config['llm']['model'],
                "messages": [{"role": "user", "content": prompt}],
                "temperature": self.config['llm']['temperature'],
                "max_tokens": self.config['llm']['max_tokens']
            }
            content_path = ["choices", 0, "message", "content"]
        else:  # completion
            payload = {
                "model": self.config['llm']['model'],
                "prompt": prompt,
                "temperature": self.config['llm']['temperature'],
                "max_tokens": self.config['llm']['max_tokens']
            }
            content_path = ["choices", 0, "text"]
        
        if provider == 'anthropic':
            # Adjust for Anthropic's format
            payload.pop("temperature", None)  # Optional tweak if needed
        
        response = requests.post(url, headers=headers, json=payload)
        print("LLM Request URL:", url)  # Debug
        print("LLM Response Status:", response.status_code)  # Debug
        print("LLM Response Text:", response.text)  # Debug
        response.raise_for_status()
        
        json_resp = response.json()
        if provider == 'anthropic':
            content = json_resp['content'][0]['text']
        else:
            # Navigate the content_path
            content = json_resp
            for key in content_path:
                if isinstance(key, int):
                    content = content[key]
                else:
                    content = content.get(key, {})
        
        # Strip unwanted delimiters like ```markdown ... ```
        content = content.strip()
        if content.startswith('```markdown'):
            content = content[len('```markdown'):].strip()
        if content.endswith('```'):
            content = content[:-3].strip()
        
        return content

    def generate_and_diff(self, code_path: str):
        rel_path = os.path.relpath(code_path, self.config['watch_dir'])
        docs_dir = os.path.join(self.config['watch_dir'], 'docs')
        os.makedirs(os.path.dirname(os.path.join(docs_dir, rel_path)), exist_ok=True)
        docs_path = os.path.join(docs_dir, rel_path + '.md')
        diff_path = os.path.join(docs_dir, rel_path + '_diff.md')
        
        old_docs = ""
        if os.path.exists(docs_path):
            with open(docs_path, 'r') as f:
                old_docs = f.read()
        
        new_docs = self.generate_docs(code_path)
        
        # Add metadata
        metadata = f"---\ngenerated_at: {time.strftime('%Y-%m-%dT%H:%M:%S')}\ncode_file: {rel_path}\n---\n\n"
        new_docs = metadata + new_docs
        
        with open(docs_path, 'w') as f:
            f.write(new_docs)
        
        if self.config['diff_output'] and old_docs:
            diff = '\n'.join(difflib.unified_diff(
                old_docs.splitlines(), new_docs.splitlines(),
                fromfile='old_docs.md', tofile='new_docs.md'
            ))
            with open(diff_path, 'w') as f:
                f.write(diff)
            self.notify(f"Diff saved to {diff_path}")

    def notify(self, message: str):
        if self.config['notify'] == 'console':
            print(message)
        elif self.config['notify'] == 'file':
            with open('doc_watcher.log', 'a') as f:
                f.write(f"{message}\n")

def main():
    parser = argparse.ArgumentParser(description="Automated code doc watcher for DiffLore.")
    parser.add_argument("--config", default="config.yaml", help="Path to config file")
    args = parser.parse_args()
    
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)
    
    event_handler = DocHandler(config)
    observer = Observer()
    observer.schedule(event_handler, path=config['watch_dir'], recursive=True)
    observer.start()
    
    print(f"Watching {config['watch_dir']} for changes...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()