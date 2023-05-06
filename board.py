"""Module providing function randrange()"""
import random
from tkinter import filedialog


class Board:
    """Class which represents a board"""

    def __init__(self, cols, rows, automaton):
        self.cols = cols
        self.rows = rows
        self.automaton = automaton
        self.current_board = None
        self.next_board = None

    def create_board(self):
        """Initialize board and its copy with dead cells."""
        self.current_board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.next_board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def create_random_board(self):
        """Create a board with random living and dead cells."""
        self.current_board = [
            [random.randrange(len(self.automaton["transition"])) for _ in range(self.cols)] for _ in range(self.rows)
        ]

    def count_neighbours(self, row0, column0):
        """Count the number of living neighbours for a given cell."""
        neighbours = [0] * len(self.automaton["transition"])
        for d_row in range(-1, 2):
            for d_col in range(-1, 2):
                if d_row != 0 or d_col != 0:
                    row = (row0 + d_row) % self.rows
                    column = (column0 + d_col) % self.cols
                    neighbours[self.current_board[row][column]] += 1
        return neighbours

    def compute_next_board(self):
        """Compute the next state of the board based on the current state."""
        for row, row_values in enumerate(self.current_board):
            for col, cell_value in enumerate(row_values):
                neighbours = self.count_neighbours(row, col)
                try:
                    self.next_board[row][col] = self.automaton["transition"][cell_value][
                        "".join(str(n) for n in neighbours)
                    ]
                except KeyError:
                    self.next_board[row][col] = self.automaton["transition"][cell_value]["default"]

    def save_board(self):
        """Saves current state of the board as .txt file"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                for row in self.current_board:
                    f.write(" ".join(str(cell) for cell in row) + "\n")

    def load_board(self):
        """Loads state of the bord from .txt file"""
        file_path = filedialog.askopenfilename(
            defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                for i, row in enumerate(f.readlines()):
                    for j, cell in enumerate(row.strip().split(" ")):
                        self.current_board[i][j] = int(cell)
