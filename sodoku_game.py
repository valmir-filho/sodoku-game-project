from tkinter import messagebox
import random
import tkinter as tk


class Sudoku:

  
    def __init__(self):
        self.board = [[0]*9 for _ in range(9)]
        self.generate_sudoku()

  
    def generate_sudoku(self):
        self.fill_values()
        self.remove_numbers()

  
    def fill_values(self):
        for i in range(9):
            for j in range(9):
                num = random.randint(1, 9)
                while not self.is_valid(i, j, num):
                    num = random.randint(1, 9)
                self.board[i][j] = num

  
    def remove_numbers(self):
        count = 20  # Number of cells to remove.
        while count != 0:
            i = random.randint(0, 8)
            j = random.randint(0, 8)
            if self.board[i][j] != 0:
                self.board[i][j] = 0
                count -= 1

  
    def is_valid(self, row, col, num):
        for x in range(9):
            if self.board[row][x] == num or self.board[x][col] == num:
                return False
        startRow, startCol = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.board[i + startRow][j + startCol] == num:
                    return False
        return True

  
    def solve(self):
        empty = self.find_empty_location()
        if not empty:
            return True
        row, col = empty
        for num in range(1, 10):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.solve():
                    return True
                self.board[row][col] = 0
        return False

  
    def find_empty_location(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return (i, j)
        return None

  
    def reset_board(self):
        self.board = [[0]*9 for _ in range(9)]
        self.generate_sudoku()


class SudokuGUI:

  
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku")
        self.sudoku = Sudoku()
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self.create_widgets()

  
    def create_widgets(self):
        for i in range(9):
            for j in range(9):
                cell = tk.Entry(self.root, width=2, font=('Arial', 24), justify='center')
                cell.grid(row=i, column=j, padx=5, pady=5)
                self.cells[i][j] = cell
                if self.sudoku.board[i][j] != 0:
                    cell.insert(0, str(self.sudoku.board[i][j]))
                    cell.config(state='readonly')
        solve_button = tk.Button(self.root, text="Solve", command=self.solve_sudoku)
        solve_button.grid(row=9, column=0, columnspan=4)
        restart_button = tk.Button(self.root, text="Restart", command=self.restart_game)
        restart_button.grid(row=9, column=4, columnspan=5)

  
    def solve_sudoku(self):
        if self.sudoku.solve():
            for i in range(9):
                for j in range(9):
                    self.cells[i][j].delete(0, tk.END)
                    self.cells[i][j].insert(0, str(self.sudoku.board[i][j]))
        else:
            messagebox.showinfo("Info", "No solution exists.")

  
    def restart_game(self):
        self.sudoku.reset_board()
        for i in range(9):
            for j in range(9):
                self.cells[i][j].delete(0, tk.END)
                if self.sudoku.board[i][j] != 0:
                    self.cells[i][j].insert(0, str(self.sudoku.board[i][j]))
                    self.cells[i][j].config(state='readonly')
                else:
                    self.cells[i][j].config(state='normal')
if __name__ == "__main__":
    root = tk.Tk()
    gui = SudokuGUI(root)
    root.mainloop()
