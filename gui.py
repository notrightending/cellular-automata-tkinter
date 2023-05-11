"""Module providing GUI functionality"""
import tkinter as tk
from board import Board
from tkinter import filedialog, messagebox
import json
import os


class CellularAutomataGUI:
    """Class responsible for GUI"""

    def __init__(self, root, cols, rows, canvas_width, canvas_height):
        self.root = root
        self.cols = cols
        self.rows = rows
        self.board = None
        self.automata = None
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
        self.create_menu()
        self.create_buttons()

    def initialize_board(self):
        """Initializes the board"""
        self.board = Board(self.cols, self.rows, self.automata)
        self.board.create_board()

    def create_menu(self):
        """Creates menu for GUI"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        board_menu = tk.Menu(menubar, tearoff=0)
        automata_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Board", menu=board_menu)
        menubar.add_cascade(label="Automata", menu=automata_menu)
        board_menu.add_command(label="Save board", command=self.save_board_option)
        board_menu.add_command(label="Load board", command=self.load_board_option)
        automata_menu.add_command(label="Create automata", command=self.create_automata_option)
        automata_menu.add_command(label="Edit automata", command=self.edit_automata_option)
        automata_menu.add_command(label="Load automata", command=self.load_automata_option)

    def save_board_option(self):
        """Saves state of the board as .txt file"""
        self.simulation_running = False
        self.board.save_board()

    def load_board_option(self):
        """Loads .txt file as a state of the board"""
        self.simulation_running = False
        self.board.load_board()
        self.render()

    def automata_window_setup(self, title, content):
        """GUI for automata creation"""
        automata_window = tk.Toplevel()
        automata_window.title(title)
        automata_window.geometry("800x600")
        text_widget = tk.Text(automata_window)
        text_widget.insert(tk.END, content)
        text_widget.pack()
        filename_entry = tk.Entry(automata_window)
        filename_entry.pack()
        return automata_window, text_widget, filename_entry

    def save_and_close(self, text_widget, filename_entry, automata_window):
        """Save and closing functionality for automaton"""
        filename = filename_entry.get()
        if filename:
            edited_content = text_widget.get(1.0, tk.END)
            with open(os.path.join("automata/", f"{filename}.json"), "w", encoding="utf-8") as file:
                file.write(edited_content)
            messagebox.showinfo("Success", "The content has been saved.")
            automata_window.destroy()
        else:
            messagebox.showerror("Error", "Please enter a valid file name.")

    def create_automata_option(self):
        """Responsible for creating new automata from template"""

        with open("automata/template.json", "r", encoding="utf-8") as file:
            template = json.load(file)
        content = json.dumps(template)
        automata_window, text_widget, filename_entry = self.automata_window_setup("Create Automata", content)
        save_button = tk.Button(
            automata_window,
            text="Save",
            command=lambda: self.save_and_close(text_widget, filename_entry, automata_window),
        )
        save_button.pack()
        close_button = tk.Button(automata_window, text="Close", command=automata_window.destroy)
        close_button.pack()

    def edit_automata_option(self):
        """Responsible for editing .json"""
        file_path = filedialog.askopenfilename(
            initialdir="automata/", defaultextension=".json", filetypes=[("Text Files", "*.json"), ("All Files", "*.*")]
        )
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                content = json.load(file)

            content_str = json.dumps(content)
            automata_window, text_widget, filename_entry = self.automata_window_setup("Edit Automata", content_str)

            text_widget.bind(
                "<FocusOut>", lambda event: self.save_and_close(text_widget, filename_entry, automata_window)
            )
            save_button = tk.Button(
                automata_window,
                text="Save",
                command=lambda: self.save_and_close(text_widget, filename_entry, automata_window),
            )
            save_button.pack()
            close_button = tk.Button(automata_window, text="Close", command=automata_window.destroy)
            close_button.pack()
        else:
            messagebox.showerror("Error", "No file selected.")

    def load_automata(self):
        """Loads state of the bord from .txt file"""
        file_path = filedialog.askopenfilename(
            initialdir="automata/", defaultextension=".json", filetypes=[("Text Files", "*.json"), ("All Files", "*.*")]
        )
        if file_path:
            with open(file_path, encoding="utf-8") as f:
                self.automata = json.load(f)

    def load_automata_option(self):
        """Loads automaton as an automata for current board"""
        self.load_automata()
        self.initialize_board()
        self.create_color_listbox()
        self.render()

    def create_buttons(self):
        """Creates buttons for GUI"""
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
            self.root.after(100, self.run_simulation)

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
