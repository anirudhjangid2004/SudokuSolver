import numpy as np


def Print(matrix):
  for i in range(9):
    print(matrix[i])

def possible(grid, x, y, n):
    for i in range(0, 9):
        if grid[i][x] == n and i != y: 
            return False

    for i in range(0, 9):
        if grid[y][i] == n and i != x: 
            return False

    x0 = (x // 3) * 3
    y0 = (y // 3) * 3
    for X in range(x0, x0 + 3):
        for Y in range(y0, y0 + 3):  
            if grid[Y][X] == n:
                return False    
    return True

# global new
new = np.zeros((9, 9), dtype=int)
def solve(grid):
    # global grid
    for y in range(9):
        for x in range(9):
            if grid[y][x] == 0:
                for n in range(1, 10):
                    if possible(grid, x, y, n):
                        grid[y][x] = n
                        
                        if solve(grid):
                            return True
                        grid[y][x] = 0  
                return False  
    return True 


# if solve(grid_n):
#     print("Solution found:")
#     print(grid_n)
# else:
#     print("No solution exists.")

