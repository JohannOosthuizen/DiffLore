import os
import tkinter as tk
from tkinter import ttk

class FileTree(ttk.Frame):
    def __init__(self, parent, on_file_select):
        super().__init__(parent)
        self.on_file_select = on_file_select

        self.tree = ttk.Treeview(self)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def populate_tree(self, directory):
        self.tree.delete(*self.tree.get_children())
        self.directory = directory
        self.process_directory("", directory)

    def process_directory(self, parent, path):
        for p in os.listdir(path):
            abs_path = os.path.join(path, p)
            isdir = os.path.isdir(abs_path)
            if p.endswith(".md") or isdir:
                oid = self.tree.insert(parent, "end", text=p, open=False)
                if isdir:
                    self.process_directory(oid, abs_path)

    def on_tree_select(self, event):
        selected_item = self.tree.selection()[0]
        path = self.get_full_path(selected_item)
        if os.path.isfile(path):
            self.on_file_select(path)

    def get_full_path(self, item):
        path = [self.tree.item(item, "text")]
        parent = self.tree.parent(item)
        while parent:
            path.insert(0, self.tree.item(parent, "text"))
            parent = self.tree.parent(parent)
        return os.path.join(self.directory, *path)
