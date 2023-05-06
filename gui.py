import tkinter as tk
from board import create_board, create_random_board, compute_next_board


class GameOfLifeGUI:
    def __init__(self, root, cols, rows, canvas_width, canvas_height):
        self.root = root
        self.cols = cols
        self.rows = rows
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.cell_height = canvas_height // rows
        self.cell_width = canvas_width // cols
        self.current_board = create_board(cols, rows)
        self.next_board = create_board(cols, rows)
        self.simulation_running = False
        self.rectangle_id_to_cell = {}
        self.initialize_gui()

    def initialize_gui(self):
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack(anchor=tk.CENTER, expand=True)
        self.create_buttons()
        self.render(self.current_board)

    def create_buttons(self):
        button_frame = tk.Frame(self.root)
        button_next = tk.Button(button_frame, text="Next step", command=self.button_next_func)
        button_random = tk.Button(button_frame, text="Randomize", command=self.button_random_func)
        button_simulate = tk.Button(button_frame, text="Simulate", command=self.button_simulate_func)
        button_clear = tk.Button(button_frame, text="Clear", command=self.button_clear_func)
        button_next.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5)
        button_random.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5)
        button_simulate.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5)
        button_clear.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5)
        button_frame.pack()
        button_frame.place(anchor=tk.CENTER, relx=0.5, rely=0.98)

    def button_next_func(self):
        compute_next_board(2, self.current_board, self.next_board)
        self.current_board, self.next_board = self.next_board, self.current_board
        self.render(self.current_board)

    def button_simulate_func(self):
        if self.simulation_running == False:
            self.simulation_running = True
            self.run_simulation()
        else:
            self.simulation_running = False

    def run_simulation(self):
        if self.simulation_running:
            self.button_next_func()
            self.root.after(100, self.run_simulation)

    def button_random_func(self):
        self.simulation_running = False
        self.current_board = create_random_board(self.cols, self.rows)
        self.render(self.current_board)

    def button_clear_func(self):
        self.simulation_running = False
        self.current_board = create_board(self.cols, self.rows)
        self.render(self.current_board)

    def render(self, board):
        self.canvas.delete("all")
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * self.cell_width
                y = row * self.cell_height
                if self.current_board[row][col] == 1:
                    fill_color = "black"
                else:
                    fill_color = "white"
                rectangle_id = self.canvas.create_rectangle(
                    x,
                    y,
                    x + self.cell_width,
                    y + self.cell_height,
                    width=1,
                    outline="gray",
                    fill=fill_color,
                )
                self.rectangle_id_to_cell[rectangle_id] = (row, col)
                self.canvas.tag_bind(
                    rectangle_id,
                    "<Button-1>",
                    lambda e, rect_id=rectangle_id: self.on_rectangle_click(rect_id),
                )

    def on_rectangle_click(self, rect_id):
        row, col = self.rectangle_id_to_cell[rect_id]
        if self.current_board[row][col] == 1:
            self.current_board[row][col] = 0
        else:
            self.current_board[row][col] = 1
        self.render(self.current_board)
