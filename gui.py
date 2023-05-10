"""Module providing GUI functionality"""
import tkinter as tk


class GameOfLifeGUI:
    """Class responsible for GUI"""

    def __init__(self, root, cols, rows, canvas_width, canvas_height, board):
        self.root = root
        self.cols = cols
        self.rows = rows
        self.board = board
        self.board.create_board()
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.cell_height = canvas_height // rows
        self.cell_width = canvas_width // cols
        self.simulation_running = False
        self.current_color_index = 0
        self.rectangle_id_to_cell = {}
        self.rectangle_ids = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.initialize_gui()

    def render(self):
        """Renders the board"""
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * self.cell_width
                y = row * self.cell_height
                fill_color = self.board.automaton["state_color"][self.board.current_board[row][col]]
                if self.rectangle_ids[row][col] is None:
                    rectangle_id = self.canvas.create_rectangle(
                        x,
                        y,
                        x + self.cell_width,
                        y + self.cell_height,
                        width=1,
                        outline="gray",
                        fill=fill_color,
                    )
                    self.rectangle_ids[row][col] = rectangle_id
                    self.rectangle_id_to_cell[rectangle_id] = (row, col)
                    self.canvas.tag_bind(
                        rectangle_id,
                        "<Button-1>",
                        lambda e, rect_id=rectangle_id: self.on_rectangle_click(rect_id),
                    )
                else:
                    rectangle_id = self.rectangle_ids[row][col]
                    self.canvas.itemconfig(rectangle_id, fill=fill_color)

    def initialize_gui(self):
        """Initializes GUI"""
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack(anchor=tk.CENTER, expand=True)
        self.create_buttons()
        self.create_color_listbox()
        self.render()

    def create_buttons(self):
        """Creates buttons for GUI"""
        button_frame = tk.Frame(self.root)
        button_next = tk.Button(button_frame, text="Next step", command=self.button_next_func)
        button_random = tk.Button(button_frame, text="Randomize", command=self.button_random_func)
        button_simulate = tk.Button(button_frame, text="Simulate", command=self.button_simulate_func)
        button_clear = tk.Button(button_frame, text="Clear", command=self.button_clear_func)
        button_save = tk.Button(button_frame, text="Save", command=self.button_save_func)
        button_load = tk.Button(button_frame, text="Load", command=self.button_load_func)
        button_save.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5)
        button_load.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5)
        button_next.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5)
        button_random.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5)
        button_simulate.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5)
        button_clear.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5)
        button_frame.pack()
        button_frame.place(anchor=tk.CENTER, relx=0.5, rely=0.98)

    def button_next_func(self):
        """Creates next iteration of a board"""
        self.board.compute_next_board()
        self.board.current_board, self.board.next_board = self.board.next_board, self.board.current_board
        self.render()

    def button_simulate_func(self):
        """Changes state of flag responsible for simulation(on/off) also calls run_simulation method"""
        if not self.simulation_running:
            self.simulation_running = True
            self.run_simulation()
        else:
            self.simulation_running = False

    def run_simulation(self):
        """Calls 'button_next_func' method continiously"""
        if self.simulation_running:
            self.button_next_func()
            self.root.after(10, self.run_simulation)

    def button_random_func(self):
        """Fills board with random states"""
        self.simulation_running = False
        self.board.create_random_board()
        self.render()

    def button_clear_func(self):
        """Clears entire board"""
        self.simulation_running = False
        self.board.create_board()
        self.render()

    def button_save_func(self):
        """Saves state of the board as .txt file"""
        self.simulation_running = False
        self.board.save_board()

    def button_load_func(self):
        """Loads .txt file as a state of the board"""
        self.simulation_running = False
        self.board.load_board()
        self.render()

    def create_color_listbox(self):
        """Creates a Listbox for choosing colors"""
        listbox_frame = tk.Frame(self.root)
        color_listbox = tk.Listbox(listbox_frame, height=len(self.board.automaton["state_color"]))
        for i, color in enumerate(self.board.automaton["state_color"]):
            color_listbox.insert(i, color)
        color_listbox.bind("<<ListboxSelect>>", self.on_color_listbox_select)
        color_listbox.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5)
        listbox_frame.pack()
        listbox_frame.place(anchor=tk.CENTER, relx=0.1, rely=0.7)

    def on_color_listbox_select(self, event):
        """Sets the current color index when a color is selected in the Listbox"""
        widget = event.widget
        self.current_color_index = widget.curselection()[0]

    def on_rectangle_click(self, rect_id):
        """Changes state of a cell on click"""
        row, col = self.rectangle_id_to_cell[rect_id]
        self.board.current_board[row][col] = self.current_color_index
        self.render()
