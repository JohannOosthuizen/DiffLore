---
generated_at: 2025-10-20T22:43:22
code_file: app\app.py
---

# Markdown Documentation Viewer - Application Documentation

## Overview

This application provides a graphical user interface (GUI) for browsing and viewing Markdown documentation files within a specified directory. It allows users to select a root directory, displays the file structure in a tree view, and opens selected `.md` files in a dedicated viewer panel. This is intended as a standalone tool for developers or technical writers needing easy access to documentation sets.

## Key Components

*   **`App(tk.Tk)`**: The main application class.
    *   **Inputs:** None (initializes the Tkinter window).
    *   **Outputs:** A Tkinter GUI application.
    *   **Logic:** Sets up the main window, paned window for splitting screen space, file tree view, markdown viewer and a directory selection button.  Handles initial setup of UI elements.
*   **`FileTree(frame, on_file_select)`**: (Located in `file_tree.py`) Displays a hierarchical tree view of files within a specified directory.
    *   **Inputs:** A parent frame (`frame`), and a callback function (`on_file_select`).
    *   **Outputs:**  A Tkinter Treeview widget displaying the file structure.
    *   **Logic:** Populates the tree with files from the given directory; triggers `on_file_select` when a file is selected.
*   **`MarkdownViewer(frame)`**: (Located in `markdown_viewer.py`) Displays Markdown content rendered as HTML within a frame.
    *   **Inputs:** A parent frame (`frame`).
    *   **Outputs:**  A Tkinter widget displaying formatted markdown.
    *   **Logic:** Renders the provided markdown file into an HTML format and displays it in a text widget.
*   **`select_directory()`**: Method within `App`.
    *   **Inputs:** None.
    *   **Outputs:** Populates the `FileTree` with files from the selected directory.
    *   **Logic:** Opens a file dialog to select a directory, then calls `file_tree.populate_tree()` to update the tree view.
*   **`on_file_select(file_path)`**: Method within `App`.
    *   **Inputs:** The path of the selected file.
    *   **Outputs:** Displays the contents of the selected markdown file in the `MarkdownViewer`.
    *   **Logic:** Calls `markdown_viewer.display_markdown()` to render and show the content of the specified Markdown file.

## Dependencies

*   **`tkinter`**: (Version not specified) - Python's standard GUI library.
*   **`tkinter.filedialog`**: For directory selection dialog.
*   **`tkinter.ttk`**: Provides themed Tkinter widgets.
*   **`.file_tree.FileTree`**:  (Defined in `file_tree.py`) – Manages the file tree display. *Reverse Dependency: App uses FileTree.*
*   **`.markdown_viewer.MarkdownViewer`**: (Defined in `markdown_viewer.py`) – Handles Markdown rendering and display. *Reverse Dependency: App uses MarkdownViewer.*

## Edge Cases

*   **Invalid Directory:** If the user selects an invalid or inaccessible directory, the `FileTree` will likely fail to populate with an error message.
*   **Non-Markdown Files:** Selecting a non-Markdown file will likely result in an error within the `MarkdownViewer`.  No specific handling is implemented for this case.
*   **Large Markdown Files:** Rendering extremely large markdown files could lead to performance issues or GUI freezes.
*   **File Permissions:** The application requires read permissions for all files and directories it accesses.

## Rationale

The architecture uses a PanedWindow to provide a split-screen view, maximizing screen real estate.  Tkinter's `ttk` widgets are used for consistent styling across platforms. Separate modules (`file_tree.py`, `markdown_viewer.py`) promote modularity and code reusability. The design prioritizes simplicity and ease of use over advanced features like live preview or syntax highlighting, which could be added in future iterations.