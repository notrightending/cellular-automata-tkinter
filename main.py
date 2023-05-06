"""Modules providing GUI functionality and parsing json"""
import tkinter as tk
import json

from gui import GameOfLifeGUI
from board import Board

COLS = 60
ROWS = 60

with open("automata/brianbrain.json", encoding="utf-8") as json_file:
    automaton = json.load(json_file)

if __name__ == "__main__":
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}")
    root.title("Conway's game of life")
    canvas_width = screen_width / 1.6
    canvas_height = screen_height / 1.2
    board = Board(COLS, ROWS, automaton["Automata"])
    gui = GameOfLifeGUI(root, COLS, ROWS, canvas_width, canvas_height, board)
    root.mainloop()
