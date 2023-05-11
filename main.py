"""Modules providing GUI functionality"""
import tkinter as tk
from gui import CellularAutomataGUI

COLS = 60
ROWS = 60


if __name__ == "__main__":
    root = tk.Tk()
    root.option_add("*tearOff", False)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}")
    root.title("Cellular automata")
    canvas_width = screen_width / 1.6
    canvas_height = screen_height / 1.2
    gui = CellularAutomataGUI(root, COLS, ROWS, canvas_width, canvas_height)
    root.mainloop()
