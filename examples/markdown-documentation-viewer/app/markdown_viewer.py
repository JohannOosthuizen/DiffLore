import tkinter as tk
from tkinter import ttk
import markdown2
from PIL import Image, ImageTk

class MarkdownViewer(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.text_area = tk.Text(self, wrap=tk.WORD, bg="#f0f0f0", bd=0, padx=10, pady=10)
        self.text_area.pack(fill=tk.BOTH, expand=True)

    def display_markdown(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                markdown_content = f.read()
            
            html_content = markdown2.markdown(markdown_content, extras=["fenced-code-blocks", "tables"])

            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, html_content)

        except Exception as e:
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, f"Error reading file: {e}")
