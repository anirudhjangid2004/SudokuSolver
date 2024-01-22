import numpy as np
import cv2 as cv

# grid = [
#     [5, 0, 0, 0, 0, 0, 9, 0, 0],
#     [0, 0, 4, 6, 9, 0, 0, 0, 0],
#     [0, 0, 0, 0, 1, 4, 0, 6, 2],
#     [0, 4, 7, 3, 6, 0, 2, 5, 8],
#     [0, 9, 8, 1, 7, 5, 4, 0, 6],
#     [0, 3, 5, 0, 0, 2, 0, 0, 0],
#     [4, 0, 0, 7, 0, 0, 0, 9, 5],
#     [0, 0, 6, 0, 0, 1, 0, 0, 0],
#     [7, 0, 2, 0, 0, 0, 6, 0, 3]
# ]

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

  x0 = (x//3) * 3
  y0 = (y//3) * 3

  for X in range(x0, x0 + 3):
    for Y in range(y0, y0 + 3):
      if grid[Y][X] == n:
        return False

  return True

def solve(grid):
  for y in range(9):
    for x in range(9):
      if grid[y][x] == 0:
        for i in range(1, 10):
          if possible(grid, x, y, i):
            grid[y][x] = i
            solve()
            grid[y][x] = 0
        return
        

  Print(grid)
  input('More?')
#   print("Ho gya lagta hai")
  
# solve(grid)
# print("Ho gya")
# print(grid)