from tkinter import ttk, DoubleVar
import tkinter as tk
from utils.ComponentUtil import ComponentUtil as cu

class CustomScale(ttk.Frame):


    def __init__(self, parent, row, column, text, range: tuple, digit):
        super().__init__(parent)

        self.grid(row=row, column=column, pady=5, padx=5, sticky=tk.W)


        self.lblText = ttk.Label(self, text=text)
        cu.place_component(self.lblText, 0, 0)


        self.value = DoubleVar()
        self.scale = ttk.Scale(
            self,
            variable=self.value,
            from_=range[0],
            to=range[1],
            command=lambda x=self.value: self._roundValue(x, digit),
            orient=tk.HORIZONTAL,

        )
        cu.place_component(self.scale, 1, 0, tk.W)

        self.lblValue = ttk.Label(self, textvariable=self.value)
        cu.place_component(self.lblValue, 1, 1)


    def _roundValue(self, value, digit):
        self.value.set(round(float(value), digit))








