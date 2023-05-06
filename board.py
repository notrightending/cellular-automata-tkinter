import random


def create_board(cols, rows):
    """Initialize board with dead cells."""
    board = [[0 for _ in range(cols)] for _ in range(rows)]
    return board


def create_random_board(cols, rows):
    """Create a board with random living and dead cells."""
    board = [[random.randint(0, 1) for _ in range(cols)] for _ in range(rows)]
    return board


def count_neighbours(row0, column0, board, states):
    """Count the number of living neighbours for a given cell."""
    neighbours = [0] * states
    for d_row in range(-1, 2):
        for d_col in range(-1, 2):
            if d_row != 0 or d_col != 0:
                row = row0 + d_row
                column = column0 + d_col
                if 0 <= row < len(board) and 0 <= column < len(board[row]):
                    neighbours[board[row][column]] += 1
    return neighbours


def compute_next_board(states, current_board, next_board):
    """Compute the next state of the board based on the current state."""
    DEAD = 0
    ALIVE = 1
    for row in range(len(current_board)):
        for col in range(len(current_board[row])):
            neighbours = count_neighbours(row, col, current_board, states)
            if current_board[row][col] == ALIVE:
                if neighbours[ALIVE] == 2 or neighbours[ALIVE] == 3:
                    next_board[row][col] = ALIVE
                else:
                    next_board[row][col] = DEAD
            elif current_board[row][col] == DEAD:
                if neighbours[ALIVE] == 3:
                    next_board[row][col] = ALIVE
                else:
                    next_board[row][col] = DEAD
