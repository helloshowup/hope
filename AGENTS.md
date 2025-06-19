# AGENTS.MD for Showup Editor UI Project

## 1. Project Overview
This project is the **Showup Editor UI**, a desktop application designed to provide a user interface for interacting with content libraries and AI-powered editing tools. It is intended for **personal, single-user operation**. The primary interface is built with **Tkinter**.

## 2. Project Structure
*   **Project Root**: `C:\Users\User\Documents\hope` (or `/workspace/hope` in Codex). This is the directory containing this `AGENTS.MD` file. All commands and development should be rooted here.
*   **Main Application Module**: `claude_panel.main`. This is the entry point launched with `python -m claude_panel.main`.ope\showup-editor-ui\launch_modular_editor.bat
*   **Core UI and Logic Packages**:
    *   `showup-editor-ui/claude_panel/`: Contains the main Tkinter UI (`main_panel.py`), application logic, configuration management (`config_manager.py`), and various helper modules.
    *   `showup-core/`: Provides core functionalities, including API interactions (e.g., `claude_api.py`).
    *   `showup-tools/`: Contains supplementary tools and utilities.
*   **User Data and Configuration**:
    *   `showup-editor-ui/settings.json`: Stores user-specific configurations, including paths to content libraries. Paths in this file are relative to the project root for portability.
    *   `showup-library/`: Default location for user content, including `library/`, `prompts/`, and `templates/`.
    *   `showup-tools/.env`: May contain API keys or other secrets for tools. In Codex, these are managed as environment secrets.

## 3. Coding Standards & Best Practices
Adherence to these standards is crucial for maintaining code quality, readability, and consistency, especially for a personal project that may evolve over time.

*   **PEP 8 Compliance**:
    *   Follow Python Enhancement Proposal 8 (PEP 8) for all Python code.
    *   Naming Conventions: `snake_case` for functions, methods, and variables; `PascalCase` for classes.
    *   Line Length: Maximum 79 characters per line is preferred.
    *   Imports: Group imports (standard library, third-party, local application) separated by blank lines.
*   **Type Hinting**:
    *   Provide type hints for all function and method signatures (parameters and return types) using the `typing` module.
    *   Strive for specific types (e.g., `List[str]`, `Optional[int]`) over `Any`.
*   **Error Handling & Resilience**:
    *   **Fail-Fast**: Raise or propagate exceptions immediately upon encountering unexpected conditions. Avoid silent failures or overly broad `try-except` blocks that mask issues.
    *   **Specific Exceptions**: Catch specific exceptions rather than generic `Exception`.
    *   **User Feedback**: For a desktop application, ensure errors are communicated clearly to the user, e.g., through dialog boxes or status bar messages, rather than just console logs.
*   **Modularity & Single Responsibility**:
    *   Modules and classes should have a single, well-defined responsibility.
    *   Break down functions/methods longer than ~30-40 lines into smaller, manageable units.
*   **Readability**:
    *   Write clear, concise, and self-documenting code.
    *   Use descriptive names for variables, functions, and classes.
*   **No Empty Blocks**:
    *   If a function, class, or method body is intentionally empty, use the `pass` statement.
*   **Logging**:
    *   Implement descriptive logging (e.g., to `showup-editor-ui/output_library_editor.log`) to aid in debugging.
*   **Tkinter Best Practices**:
    *   Separate UI layout from business logic where possible.
    *   Be mindful of the main UI thread; long-running operations should be offloaded to separate threads or asynchronous tasks to prevent freezing the UI. (Refer to MEMORY[f0fd4cfe-44e0-4d24-817e-d7c323de76b4] for known issues in `enrich_lesson.py`).
    *   Ensure thread-safe updates to Tkinter widgets if using multi-threading (e.g., using `queue` module or `after` method).

## 4. Dependencies & Environment
*   **Python**: The project is developed in Python (version 3.12 used in Codex).
*   **Key Python Packages**:
    *   `tkinter` (standard library): For the main GUI.
    *   `PyQt5` (optional, listed in requirements but primary UI is Tkinter).
    *   `anthropic`, `langchain`, `sentence-transformers`, `faiss-cpu`: For AI and RAG functionalities.
    *   See `showup-editor-ui/requirements.txt` and `showup-core/requirements.txt` for full lists.
*   **Environment Variables & Secrets**:
    *   API keys or other sensitive configurations might be used by `showup-core` or `showup-tools`.
    *   Locally, these might be in `.env` files (e.g., `showup-tools/.env`).
    *   In the Codex environment, these are managed as "Secrets".
    *   **Focus on Single User**: Configuration and secrets management should be straightforward, suitable for a single user managing their own environment. Avoid complexity aimed at multi-tenant or production systems.

## 5. Running & Testing the Application
*   **Launch Method (Codex & Local)**:
    *   Ensure `PYTHONPATH` is set correctly to include project root, `showup-core`, and `showup-tools`.
    *   From the project root (`/workspace/hope` or `C:\Users\User\Documents\hope`):
        ```bash
        python -m claude_panel.main
        ```
*   **Setup**:
    *   Dependencies are installed via `pip install -r <requirements_file>` and `pip install -e ./showup-core` as defined in the Codex setup script.
*   **Testing**:
    *   Manual testing of UI workflows is primary for this personal-use application.
    *   Focus on core functionality: loading libraries, interacting with AI features, saving outputs.

## 6. Code Modification Guidelines
*   **Atomic Commits/Changes**: Group related code changes into single, logical units.
*   **Dependency Analysis**: Before moving or refactoring modules/files, analyze imports.
*   **Immediate Reference Updates**: After moving or renaming code, update all import statements.
*   **Continuous Validation**: After significant changes, run the application to test core workflows.
*   **Preserve Workflow & Behavior**: Refactoring should not alter existing user-facing behavior unless intended.

## 7. AI Assistant (Cascade) Interaction Protocol
*   **Contextual Adherence**: This `AGENTS.MD` file provides the primary context for your operations within this project. The focus is on a **single-user desktop application**. Avoid suggesting enterprise-grade or web-scale solutions unless specifically requested.
*   **Tool Usage**: When using tools (e.g., proposing code changes), ensure your actions align with the project's structure and the coding standards outlined here.
*   **Memory Utilization**: Actively use and refer to project-specific memories (like MEMORY[f0fd4cfe-44e0-4d24-817e-d7c323de76b4] regarding threading in `enrich_lesson.py`) to maintain continuity and address known issues.
*   **Clarification**: If any instruction in this document or a user request is ambiguous, seek clarification before proceeding.
*   **Simplicity for Personal Use**: Prioritize straightforward solutions suitable for a personal project. For example, complex CI/CD pipelines or overly elaborate testing frameworks are likely unnecessary.

## 8. Launch & Import Notes
*   `showup-editor-ui\launch_modular_editor.bat` is the **only** batch scripts used to start the application. Remove any other `.bat` files to avoid confusio expect for and showup-editor-ui\run_podcast_generator.bat
*   Import paths rely on underscores (e.g., `claude_panel`, `showup_tools`). Typos with hyphens like `claude-panel` or `showup-tools` will break imports.
