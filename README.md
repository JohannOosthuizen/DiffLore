# DiffLore

[![GitHub license](https://img.shields.io/github/license/yourusername/difflore)](https://github.com/yourusername/difflore/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/yourusername/difflore)](https://github.com/yourusername/difflore/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/yourusername/difflore)](https://github.com/yourusername/difflore/issues)

AI-powered code documentation watcher. Automates Markdown generation, semantic diffing, & interdependency mapping for AI coding workflows. Real-time file monitoring enhances Fridman's loop with structured insights. Keeps codebase organized & maintainable. Python-built, LLM-compatible (Grok, OpenAI, Anthropic). Tame AI chaos, boost productivity! 🚀

## Features
- **Real-Time Monitoring**: Watches project directories for code changes using `watchdog`.
- **Automated Doc Generation**: Uses LLMs to create structured Markdown docs (overview, components, dependencies, edge cases, rationale).
- **Semantic Diffing**: Computes and saves unified diffs of docs for quick semantic reviews.
- **Interdependency Mapping**: Parses imports and relationships, injecting hints for comprehensive docs.
- **Flexible Configuration**: YAML-based setup for LLMs, prompts, file patterns, and more.
- **Hierarchical Organization**: Mirrors code structure in `/docs/` with metadata and cross-links.
- **Inspired by Lex Fridman**: Enhances AI-assisted coding loops by adding doc steps for better understanding and maintainability.

## Installation
1. Clone the repo:
   ```
   git clone https://github.com/yourusername/difflore.git
   cd difflore
   ```
2. Install dependencies:
   ```
   pip install watchdog requests pyyaml
   ```
3. Set up LLM API keys in environment variables (e.g., `GROK_API_KEY`).

## Usage
1. Configure `config.yaml` (see example in repo).
2. Run the watcher:
   ```
   python auto_doc_watcher.py --config config.yaml
   ```
3. Edit code files—docs and diffs auto-generate in `/docs/`.

## Configuration
Edit `config.yaml` for watch dir, LLM provider, prompt templates, etc. Example:
```yaml
watch_dir: ./my_project
file_patterns: ['*.py']
llm:
  provider: grok
  api_key: your_key
prompt_template: |-
  # Your custom prompt here
```

## Contributing
Pull requests welcome! Fork, create a branch, commit changes, and submit a PR. Follow standard Python style (PEP8).

## License
MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments
Inspired by Lex Fridman's AI coding insights and teachableai's doc-diff ideas. Built with xAI's Grok in mind.
