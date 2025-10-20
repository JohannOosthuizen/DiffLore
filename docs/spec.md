# DiffLore Project Specification

## Version History
- **v1.0**: Initial draft - October 20, 2025.
- **v1.1**: Incorporated best practices from software specification guidelines, including clarity, SMART criteria for requirements, glossary, traceability, and stakeholder review processes - Refined on [Current Date].

This document is a living artifact and will be updated collaboratively as the project evolves. Use a collaborative editor (e.g., Google Docs or GitHub Markdown) for reviews and iterations.

## 1. Introduction

### 1.1 Project Overview
DiffLore is an open-source, AI-powered tool designed to enhance AI-assisted coding workflows by automating the generation, organization, and diffing of code documentation. It acts as a real-time file watcher that monitors changes in a project's codebase, generates structured Markdown documentation using large language models (LLMs), computes semantic diffs between documentation versions, and maps interdependencies across files. This addresses common pain points in modern software development, such as opaque AI-generated code, maintainability issues, and context management in agent-based tools.

The tool is built in Python and is compatible with various LLMs (e.g., Grok from xAI, OpenAI's GPT models, Anthropic's Claude, or local options like Ollama). It runs locally as a daemon process, ensuring privacy and low latency, and integrates seamlessly with IDEs, CLIs, or version control systems.

### 1.2 Key Goals
These goals are defined using SMART criteria (Specific, Measurable, Achievable, Relevant, Time-bound) to ensure clarity and trackability:
- **Improve Comprehension in AI Workflows**: Insert an automated "documentation step" into iterative coding processes, making AI outputs more verifiable and educational (Measured by reduced review time in prototypes; Achievable via LLM integration; Relevant to Fridman's process; Time-bound to MVP release).
- **Handle Interdependencies**: Automatically detect and document relationships between files, libraries, and components to provide a holistic view of the codebase (Measured by accuracy in dependency graphs; Achievable with parsers like ast; Relevant for multi-file projects; Time-bound to v0.1).
- **Enable Semantic Reviews**: Shift focus from noisy code diffs to human-readable documentation diffs for faster reviews and debugging (Measured by user feedback on diff utility; Achievable with difflib; Relevant for maintainability; Time-bound to MVP).
- **Flexibility and Scalability**: Support multiple languages, LLM providers (online/local), and project sizes without requiring extensive setup (Measured by config options and benchmarks; Achievable with modular architecture; Relevant for diverse users; Time-bound to v0.2).
- **Maintainability**: Keep generated docs organized, versioned, and concise to avoid bloat (Measured by file size limits and pruning rules; Achievable with automation; Relevant for long-term use; Time-bound to v0.1).

### 1.3 Target Audience
- Developers using AI agents (e.g., GitHub Copilot, Cursor, Gemini CLI, Claude) for code generation.
- Teams in collaborative projects needing auditable, maintainable codebases.
- Solo devs or learners seeking to accelerate understanding in Fridman-inspired loops.
- Open-source contributors interested in extending the tool for custom workflows.

### 1.4 Non-Goals
- Not a full-fledged IDE plugin (though extensible to one).
- Does not execute or test code—focuses solely on documentation.
- Avoids cloud dependencies; all processing is local except optional LLM API calls.

### 1.5 Assumptions and Constraints
- Assumptions: Users have Python 3.8+ installed; LLMs are accessible via APIs or local servers; Codebases are primarily Python initially (extensible to others).
- Constraints: Performance limited by LLM response times; No real-time execution for very large repos without async optimizations; Relies on file system access.

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
Each feature includes traceability to goals/motivation and success criteria.
- **File Watching**: Real-time monitoring of specified directories/files using `watchdog` for changes (e.g., edits from AI agents or manual). (Traceable to Goal 1; Success: <1s detection latency for small changes).
- **Automated Doc Generation**: LLM-based creation of structured Markdown docs with sections: Overview, Key Components, Dependencies, Edge Cases, Rationale. (Traceable to Goal 1; Success: Docs under 500 words, generated in <10s).
- **Dependency Mapping**: Parses code (e.g., via `ast` for Python) to extract imports/references; injects hints into prompts for accurate inter-file docs. (Traceable to Goal 2; Success: 95% accuracy in import detection).
- **Semantic Diffing**: Computes unified diffs of Markdown docs (using `difflib`) to highlight conceptual changes. (Traceable to Goal 3; Success: Diff files <1KB for typical changes).
- **Organization**: Hierarchical `/docs/` mirroring code structure, with metadata (e.g., generation timestamp, code file link) and cross-references. (Traceable to Goal 5; Success: No bloat over 10 versions without pruning).

### 3.2 Advanced Features
- **Configurable Prompts**: Customizable templates for doc structure, with LLM-specific tweaks.
- **Multi-LLM Support**: Providers like Grok, OpenAI, Anthropic; easy extension for others.
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

(Include flowchart diagram in future versions for visual clarity).

### 4.3 Tech Stack
- **Core**: Python 3.8+.
- **Dependencies**: `watchdog` (watching), `requests` (API calls), `pyyaml` (config), `difflib`/`ast` (built-in).
- **Optional Dependencies**: `ollama` (user-installed for local serving; not in core requirements.txt).
- **LLMs**: API-based; support for local models.
- **Testing**: Pytest for units (mock APIs).
- **Packaging**: `pyproject.toml` for pip installs.

## 5. Implementation Details

### 5.1 Configuration Schema
YAML file with sections (organized for clarity):
- `watch_dir`: Str (e.g., "./project").
- `file_patterns`: List[str] (e.g., ["*.py"]).
- `llm`: Dict (provider, api_key, model, temperature, max_tokens, url for local).
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
- Async calls if scaling to multiple files (future optimization).

### 5.4 Security
- Local-only by default; API keys via env vars.
- No code execution—only documentation.

## 6. Development Plan

### 6.1 Milestones
Deliverables with responsibilities and timelines:
- **MVP** (Due: 2 weeks): Core watcher, doc gen, diffing (Responsible: Lead Dev).
- **v0.1** (Due: 4 weeks): Dependency mapping, config flexibility (Responsible: Dev Team).
- **v0.2** (Due: 6 weeks): Project-wide features, tests (Responsible: QA/Dev).
- **v1.0** (Due: 8 weeks): Extensions, packaging, docs site (Responsible: All Stakeholders).

### 6.2 Testing Strategy
- Unit: Mock LLM responses, test parsing/diffing.
- Integration: Run on example projects, verify outputs.
- Manual: Simulate AI edits in a toy repo.
- Success Criteria: 100% coverage for core functions; No critical bugs in prototypes.

### 6.3 Contribution Guidelines
- Follow PEP8.
- PRs with tests/docs.
- Issues for features/bugs.
- Conduct peer reviews for all changes.

### 6.4 Communication Plan
- Weekly updates via GitHub issues/PRs.
- Stakeholder reviews at milestone ends.
- Deployment: Open-source on GitHub; Notifications via email/Slack for releases.

## 7. Risks and Mitigations
- **LLM Inaccuracy**: Refine prompts; allow user overrides (Priority: High; Mitigation: Manual edits).
- **Overhead**: Configurable scopes; optimize for small changes (Priority: Medium; Mitigation: Benchmarks).
- **Scalability**: Start sync; add async for large repos (Priority: Low; Mitigation: Profiling).
- **Dependency Changes**: Monitor libs; pin versions (Priority: Low; Mitigation: Requirements file).

## 8. Glossary
- **LLM**: Large Language Model - AI systems for text generation (e.g., Grok).
- **SRS**: Software Requirements Specification - This document.
- **MVP**: Minimum Viable Product - Initial functional release.
- **SMART**: Specific, Measurable, Achievable, Relevant, Time-bound - Criteria for goals/requirements.
- **Daemon**: Background process running continuously.

## 9. References
- Lex Fridman's Post: https://x.com/lexfridman/status/1957940412179497327
- teachableai Idea: https://x.com/teachableai/status/1980071754300092865
- Python Docs: https://docs.python.org/3/library/ast.html (for parsing)

This spec is a living document—update as the project evolves. Last updated: October 20, 2025.
