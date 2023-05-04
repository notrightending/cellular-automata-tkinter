import tkinter as tk
import random

def create_board(cols, rows):
    """Initialize board with dead cells"""
    board = []
    for r in range(rows):
        row = []
        for c in range(cols):
            row.append(0)
        board.append(row)
    return board

def create_random_board(cols, rows):
    board = []
    for r in range(rows):
        row = []
        for c in range(cols):
            row.append(random.randint(0,1))
        board.append(row)  
    return board  


COLS, ROWS = 60, 60
CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 900
current_board = create_board(COLS, ROWS)
next_board = create_board(COLS, ROWS)
def count_neighbours(row0, column0, board, states):
    neighbours = [0] * states
    for d_row in range(-1, 2):
        for d_col in range(-1, 2):
            if (d_row != 0 or d_col != 0):
                row = row0 + d_row
                column = column0 + d_col
                if (0 <= row and row < ROWS):
                    if (0 <= column and column < COLS):
                        neighbours[board[row][column]] += 1
    return neighbours

def compute_next_board(states, current_board, next_board):
    DEAD = 0
    ALIVE = 1
    neighbours = [0] * states
    for row in range(ROWS):
        for col in range(COLS):
            neighbours = count_neighbours(row, col, current_board, states)
            if (current_board[row][col] == ALIVE):
                if (neighbours[ALIVE] == 2 or neighbours[ALIVE] == 3):
                    next_board[row][col] = ALIVE
                else:
                    next_board[row][col] = DEAD
            elif (current_board[row][col] == DEAD):
                if (neighbours[ALIVE] == 3):
                    next_board[row][col] = ALIVE
                else:
                    next_board[row][col] = DEAD



CELL_HEIGHT = CANVAS_HEIGHT // ROWS
CELL_WIDTH = CANVAS_WIDTH // COLS
root = tk.Tk()
root.geometry('1280x1024')
root.title('Game of life')
canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg='white')
canvas.pack(anchor=tk.CENTER, expand=True)
simulation_running = False

def button_func():
    global current_board, next_board
    compute_next_board(2, current_board, next_board)
    current_board, next_board = next_board, current_board
    render(current_board)

def button_simulate():
    global simulation_running
    simulation_running = True
    run_simulation()

def run_simulation():
    if simulation_running:
        button_func()
        root.after(100, run_simulation)

def button_stopf():
    global simulation_running
    simulation_running = False


def button_random():
    global current_board
    current_board = create_random_board(COLS, ROWS)
    render(current_board)

def button_clearf():
    global current_board
    current_board = create_board(COLS, ROWS)
    render(current_board)

button_frame = tk.Frame(root)
button_step = tk.Button(button_frame, text='Next step', command=button_func)
button_rand = tk.Button(button_frame, text='Randomize', command=button_random)
button_sim =  tk.Button(button_frame, text='Simulate', command=button_simulate)
button_clear = tk.Button(button_frame, text='Clear', command=button_clearf)
button_stop = tk.Button(button_frame, text='Stop', command=button_stopf)
button_step.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5)
button_rand.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5)
button_sim.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5)
button_clear.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5)
button_stop.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5)
button_frame.pack()
button_frame.place(anchor=tk.CENTER, relx=0.5, rely=0.98)



rectangle_id_to_cell = {}

def render(board):
    canvas.delete("all")  # Clear the canvas before rendering
    for row in range(ROWS):
        for col in range(COLS):
            x = col * CELL_WIDTH
            y = row * CELL_HEIGHT
            if (current_board[row][col] == 1):
                fill_color = 'black'
            else:
                fill_color = 'white'
            rectangle_id = canvas.create_rectangle(x, y, x+CELL_WIDTH, y+CELL_HEIGHT, width=1, outline='gray', fill=fill_color)
            rectangle_id_to_cell[rectangle_id] = (row, col)
            canvas.tag_bind(rectangle_id, '<Button-1>', lambda e, rect_id=rectangle_id: on_rectangle_click(rect_id))


def on_rectangle_click(rect_id):
    row, col = rectangle_id_to_cell[rect_id]
    if current_board[row][col] == 1:
        current_board[row][col] = 0
    else:
        current_board[row][col] = 1
    render(current_board)

render(current_board)
root.mainloop()
