import tkinter as tk
from tkinter import filedialog, ttk
from .file_tree import FileTree
from .markdown_viewer import MarkdownViewer

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Markdown Documentation Viewer")
        self.geometry("1200x800")

        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.paned_window = ttk.PanedWindow(self.main_frame, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        self.file_tree_frame = ttk.Frame(self.paned_window, width=300)
        self.paned_window.add(self.file_tree_frame, weight=1)

        self.markdown_viewer_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(self.markdown_viewer_frame, weight=3)

        self.file_tree = FileTree(self.file_tree_frame, on_file_select=self.on_file_select)
        self.file_tree.pack(fill=tk.BOTH, expand=True)

        self.markdown_viewer = MarkdownViewer(self.markdown_viewer_frame)
        self.markdown_viewer.pack(fill=tk.BOTH, expand=True)

        self.select_dir_button = ttk.Button(self.main_frame, text="Select Documentation Directory", command=self.select_directory)
        self.select_dir_button.pack(pady=10)

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.file_tree.populate_tree(directory)

    def on_file_select(self, file_path):
        self.markdown_viewer.display_markdown(file_path)
