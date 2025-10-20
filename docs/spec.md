# DiffLore Project Specification

## 1. Introduction

### 1.1 Project Overview
DiffLore is an open-source, AI-powered tool designed to enhance AI-assisted coding workflows by automating the generation, organization, and diffing of code documentation. It acts as a real-time file watcher that monitors changes in a project's codebase, generates structured Markdown documentation using large language models (LLMs), computes semantic diffs between documentation versions, and maps interdependencies across files. This addresses common pain points in modern software development, such as opaque AI-generated code, maintainability issues, and context management in agent-based tools.

The tool is built in Python and is compatible with various LLMs (e.g., Grok from xAI, OpenAI's GPT models, Anthropic's Claude). It runs locally as a daemon process, ensuring privacy and low latency, and integrates seamlessly with IDEs, CLIs, or version control systems.

### 1.2 Key Goals
- **Improve Comprehension in AI Workflows**: Insert an automated "documentation step" into iterative coding processes, making AI outputs more verifiable and educational.
- **Handle Interdependencies**: Automatically detect and document relationships between files, libraries, and components to provide a holistic view of the codebase.
- **Enable Semantic Reviews**: Shift focus from noisy code diffs to human-readable documentation diffs for faster reviews and debugging.
- **Flexibility and Scalability**: Support multiple languages, LLM providers, and project sizes without requiring extensive setup.
- **Maintainability**: Keep generated docs organized, versioned, and concise to avoid bloat.

### 1.3 Target Audience
- Developers using AI agents (e.g., GitHub Copilot, Cursor, Gemini CLI, Claude) for code generation.
- Teams in collaborative projects needing auditable, maintainable codebases.
- Solo devs or learners seeking to accelerate understanding in Fridman-inspired loops.
- Open-source contributors interested in extending the tool for custom workflows.

### 1.4 Non-Goals
- Not a full-fledged IDE plugin (though extensible to one).
- Does not execute or test code—focuses solely on documentation.
- Avoids cloud dependencies; all processing is local except LLM API calls.

## 2. Motivation

### 2.1 Inspiration from Lex Fridman
This project is directly inspired by Lex Fridman's X post (https://x.com/lexfridman/status/1957940412179497327) on AI-assisted programming. Fridman describes an "insanely fun" iterative process:
1. Generate code with AI.
2. Read and understand the generated code.
3. Make small manual changes (with autocomplete).
4. Test and debug.
5. Make big changes with a new prompt.
6. Loop back to step 1.

He warns against "pure vibe coding" (skipping steps 2-3), which erodes human expertise, and highlights transformation in software engineering with both exciting (productivity) and scary (jobs, security) implications.

DiffLore enhances this by adding a "step 1.5": Automated documentation generation post-code-gen, serving as a proxy for understanding. This reduces cognitive load, exposes AI hallucinations early, and fosters faster learning/productivity while mitigating risks.

### 2.2 Problems Solved
- **AI Output Opacity**: AI-generated code can be verbose or idiosyncratic; docs provide a high-level map.
- **Context Management**: Tools like Gemini CLI use monolithic files (e.g., GEMINI.md); DiffLore uses dynamic, diff-aware docs to keep context lean.
- **Interdependency Blind Spots**: In multi-file projects, relationships (imports, calls) are often undocumented; automated parsing and LLM hints address this.
- **Review Bottlenecks**: Traditional code diffs are noisy; semantic doc diffs focus on intent changes.
- **Skill Erosion**: By articulating rationale and edges, docs turn AI into a teaching tool.

### 2.3 Related Ideas
- Builds on teachableai's doc-diff workflow (https://x.com/teachableai/status/1980071754300092865).
- Aligns with community feedback on Fridman's post (e.g., adding planning steps, using proxies like tests).
- Complements tools like Doxygen or Sphinx but focuses on AI-driven, real-time automation.

## 3. Features

### 3.1 Core Features
- **File Watching**: Real-time monitoring of specified directories/files using `watchdog` for changes (e.g., edits from AI agents or manual).
- **Automated Doc Generation**: LLM-based creation of structured Markdown docs with sections: Overview, Key Components, Dependencies, Edge Cases, Rationale.
- **Dependency Mapping**: Parses code (e.g., via `ast` for Python) to extract imports/references; injects hints into prompts for accurate inter-file docs.
- **Semantic Diffing**: Computes unified diffs of Markdown docs (using `difflib`) to highlight conceptual changes.
- **Organization**: Hierarchical `/docs/` mirroring code structure, with metadata (e.g., generation timestamp, code file link) and cross-references.

### 3.2 Advanced Features
- **Configurable Prompts**: Customizable templates for doc structure, with LLM-specific tweaks.
- **Multi-LLM Support**: Provider like Grok, OpenAI, Anthropic; easy extension for others.
- **Local LLM Support**: Provider option for 'ollama' (or similar local servers) to run inference without internet/cloud costs.
- **Notifications/Logging**: Console, file, or future integrations (e.g., Slack) for change alerts.
- **Pruning and Archiving**: Rules to manage doc bloat (e.g., summarize old versions via LLM).
- **Project-Wide Indexing**: Auto-generate `dependencies.md` or index.md for overviews/graphs (e.g., using Mermaid for visuals).

### 3.3 Planned Extensions
- Language Support: Add parsers for JS, Java, etc.
- Git Integration: Hooks for pre-commit doc gen/diffs.
- Visualizations: Embed call graphs or dependency diagrams in docs.
- Self-Improvement: Use LLM to refine prompts based on user feedback.

## 4. Architecture

### 4.1 High-Level Components
- **Watcher (DocHandler)**: Extends `watchdog`'s event handler; triggers on file modifications.
- **Dependency Extractor**: Language-specific parsers (start with Python `ast`); outputs hints for prompts.
- **LLM Caller**: Modular API wrappers for providers; handles prompts, responses, and errors.
- **Diff Generator**: Uses `difflib` for Markdown comparisons; saves to files.
- **Organizer**: Manages folder structure, metadata, and pruning.
- **Main Entry**: CLI script (`watcher.py`) parsing config and starting the observer.

### 4.2 Data Flow
1. User configures `config.yaml` (watch dir, LLM, patterns).
2. Watcher starts, monitors recursively.
3. On change: Extract deps → Build prompt → Call LLM → Add metadata → Save docs.md.
4. If prior docs: Compute diff → Save _diff.md → Notify.
5. Optional: Aggregate for project-wide views.

### 4.3 Tech Stack
- **Core**: Python 3.8+.
- **Dependencies**: `watchdog` (watching), `requests` (API calls), `pyyaml` (config), `difflib`/`ast` (built-in).
- **Optional Dependencies**: `ollama` (user-installed for local serving; not in core requirements.txt).
- **LLMs**: API-based; no local models initially.
- **Testing**: Pytest for units (mock APIs).
- **Packaging**: `pyproject.toml` for pip installs.

## 5. Implementation Details

### 5.1 Configuration Schema
YAML file with sections:
- `watch_dir`: Str (e.g., "./project").
- `file_patterns`: List[str] (e.g., ["*.py"]).
- `llm`: Dict (provider, api_key, model, temperature, max_tokens).
  - llm dict now supports 'ollama' as provider, with optional url: http://localhost:11434 for custom hosts.
- `prompt_template`: Str (multiline with {code} placeholder).
- `diff_output`: Bool.
- `notify`: Str ("console", "file").
- `dep_depth`: Str ("shallow" for imports only).

### 5.2 Error Handling
- Graceful retries on LLM failures (e.g., rate limits).
- Fallback to basic docs if parsing fails.
- Logging for all events.

### 5.3 Performance Considerations
- Debounce rapid changes (e.g., 5s delay).
- Token limits in prompts to control costs.
- Async calls if scaling to multiple files.

### 5.4 Performance Considerations
- Debounce rapid changes (e.g., 5s delay).
- Token limits in prompts to control costs.
- Async calls if scaling to multiple files.

### 5.4 Security
- Local-only by default; API keys via env vars.
- No code execution—only documentation.

## 6. Development Plan

### 6.1 Milestones
- **MVP**: Core watcher, doc gen, diffing (current script).
- **v0.1**: Dependency mapping, config flexibility.
- **v0.2**: Project-wide features, tests.
- **v1.0**: Extensions, packaging, docs site.

### 6.2 Testing Strategy
- Unit: Mock LLM responses, test parsing/diffing.
- Integration: Run on example projects, verify outputs.
- Manual: Simulate AI edits in a toy repo.

### 6.3 Contribution Guidelines
- Follow PEP8.
- PRs with tests/docs.
- Issues for features/bugs.

## 7. Risks and Mitigations
- **LLM Inaccuracy**: Refine prompts; allow user overrides.
- **Overhead**: Configurable scopes; optimize for small changes.
- **Scalability**: Start sync; add async for large repos.
- **Dependency Changes**: Monitor libs; pin versions.

## 8. References
- Lex Fridman's Post: https://x.com/lexfridman/status/1957940412179497327
- teachableai Idea: https://x.com/teachableai/status/1980071754300092865
- Python Docs: https://docs.python.org/3/library/ast.html (for parsing)

This spec is a living document—update as the project evolves. Last updated: October 20, 2025.