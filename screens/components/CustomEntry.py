import tkinter as tk
from tkinter import ttk
from utils.ComponentUtil import ComponentUtil as cu

class CustomEntry(ttk.Frame):

    def __init__(self, parent, row, column, text, tk_value, password=False):
        super().__init__(parent)
        self.grid(row=row, column=column, padx=5, pady=5)

        self.lbl_text = ttk.Label(self, text=text)
        cu.place_component(self.lbl_text, 0, 0)

        self.entry = ttk.Entry(self, textvariable=tk_value)
        cu.place_component(self.entry, 0, 1)

        if password:
            self.entry.config(show="*")
