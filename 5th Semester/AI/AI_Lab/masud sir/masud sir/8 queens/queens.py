# 8 Queens Problem using Backtracking

N = 8  # 8x8 chess board

# Function to print the solution
def print_solution(board):
    for row in board:
        print(" ".join(row))
    print("\n")

# Check if it's safe to place a queen
def is_safe(board, row, col):
    # Check this column
    for i in range(row):
        if board[i][col] == "Q":
            return False

    # Check upper left diagonal
    for i, j in zip(range(row-1, -1, -1), range(col-1, -1, -1)):
        if board[i][j] == "Q":
            return False

    # Check upper right diagonal
    for i, j in zip(range(row-1, -1, -1), range(col+1, N)):
        if board[i][j] == "Q":
            return False

    return True

# Solve using backtracking
def solve(board, row=0):
    if row == N:
        print_solution(board)
        return True

    for col in range(N):
        if is_safe(board, row, col):
            board[row][col] = "Q"  # Place queen
            if solve(board, row + 1):
                return True
            board[row][col] = "."  # Backtrack

    return False

# Initialize the chess board
board = [["." for _ in range(N)] for _ in range(N)]

# Solve and print
solve(board)
