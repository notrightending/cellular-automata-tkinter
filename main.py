import tkinter as tk
from gui import GameOfLifeGUI

if __name__ == "__main__":
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f'{screen_width}x{screen_height}')
    root.title("Conway's game of life")
    canvas_width = screen_width / 1.6 
    canvas_height = screen_height / 1.2
    gui = GameOfLifeGUI(root, cols=60, rows=60, canvas_width=canvas_width, canvas_height=canvas_height)
    root.mainloop()
