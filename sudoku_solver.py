import os
import time

class SudokuSolver():
    def __init__(self, board):
        self.board = board

    def _print_board(self, board, col, row):
            print("+ - - - + - - - + - - - +")
            for i in range(len(board)):
                if i % 3 == 0 and i != 0:
                    print("+ - - - + - - - + - - - +")

                for j in range(len(board[0])):
                    if j % 3 == 0:
                        print("| ", end="")
                    if i == row and j == col and j == 8:
                        print(f"\033[31m{board[i][j]}\033[0m" + " |")
                    elif j == 8:
                        print(str(board[i][j]) + " |")
                    elif i == row and j == col:
                        print(f"\033[31m{board[i][j]}\033[0m ", end="")
                    else:
                        print(f"{board[i][j]} ", end="") 
            print("+ - - - + - - - + - - - +")

    def _is_valid(self, board, num, col, row):
        """Validates if the number passed to the function follows all the constraints of sudoku and returns a bool"""
        if num in board[row]:
            return False
        for i in range(9):
            if num == board[i][col]:
                return False
        start_row = row - (row % 3)
        start_col = col - (col % 3)
        for i in range(3):
            for j in range(3):
                if num == board[i + start_row][j + start_col]:
                    return False
        return True
    
    def _find_free_space(self, board, mode):
            """Iterates throught the free spaces and checks the number of legal candidates and
            returns the cell that has the fewest legal candidates to catch deadends earlier """

            if mode == "slow":
                for i in range(9):
                    for j in range(9):
                        if board[i][j] == 0:
                            return i, j
                return False
            
            elif mode == "fast":
                best_cell = None
                best_count = 10  # more than the maximum of 9 candidates
                for i in range(9):
                    for j in range(9):
                        if board[i][j] == 0:
                            candidate_count = sum(1 for k in range(1, 10) if self._is_valid(board, k, j, i))
                            if candidate_count == 0:
                                return None  # no legal moves, so unsolvable branch
                            if candidate_count < best_count:
                                best_count = candidate_count
                                best_cell = (i, j)
                return False if best_cell is None else best_cell

    def timing(func):
        """Times the completion time of the different methods"""
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            print(f"{func.__name__} took {end_time - start_time:.4f} seconds")
            return result
        return wrapper
    

    @timing
    def slow_solve(self):

        def solve_sudoku_slow(board):
            """Recursivly trys all possible combinations within a for loop and if a deadend is reach the current candidated
                will be changed back to 0, essentially backtracking on the decision and the for loop will advance and the next
                possible candidate will be tested untill all posiblities are exhausted and the puzzle is either complete or invalid"""
            
            free = self._find_free_space(board, mode="slow")
            if not free:
                return True
            row, col = free

            # the solution trys the candidate and recursivly calls the function if true
            # if the solution hits a dead end the decision is undone with board[][] = 0
            # the for loop then tries the next possible combination until all possiblilties have been exhausted
            for num in range(1, 10):
                if self._is_valid(board, num, col, row):
                    board[row][col] = num
                    os.system('clear')
                    self._print_board(board, col, row)
                    # time.sleep(0.5)
                    if solve_sudoku_slow(board):
                        return True
                    board[row][col] = 0

            return False
        
        return solve_sudoku_slow(self.board)

    @timing 
    def fast_solve(self):
        """Utilizes a method called Minimum Remaining Values (MRV) to greatly reduces the time to solve by catching deadends earlier """
        
        def solve_sudoku_fast(board):
            free = self._find_free_space(board, mode="fast")
            if free is None:
                return False  # unsolvable branch detected
            if free is False:
                return True 
            row, col = free

            # the solution trys the candidate and recursivly calls the function if true
            # if the solution hits a dead end the decision is undone with board[][] = 0
            # the for loop then tries the next possible combination until all possiblilties have been exhausted
            for num in range(1, 10):
                if self._is_valid(board, num, col, row):
                    board[row][col] = num
                    os.system('clear')
                    self._print_board(board, col, row)
                    # time.sleep(0.5)
                    if solve_sudoku_fast(board):
                        return True
                    board[row][col] = 0    
            return False
        
        return solve_sudoku_fast(self.board)


if __name__ == "__main__":
    board = [
        [8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 6, 0, 0, 0, 0, 0],
        [0, 7, 0, 0, 9, 0, 2, 0, 0],
        [0, 5, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 4, 5, 7, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 3, 0],
        [0, 0, 1, 0, 0, 0, 0, 6, 8],
        [0, 0, 8, 5, 0, 0, 0, 1, 0],
        [0, 9, 0, 0, 0, 0, 4, 0, 0],
    ]

solve = SudokuSolver(board)

solve.fast_solve()






        
    
    









