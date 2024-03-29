import pygame
import threading

LIGHT_COLOR = 'white'
DARK_COLOR  = 'black'


class board:
    def __init__(self):
        grid = [[None for _ in range(8)] for _ in range(8)]
        gridLocks =  [[threading.Lock for _ in range(8)] for _ in range(8)]
        
        grid[0][0] = Rook(DARK_COLOR)
        grid[7][0] = Rook(DARK_COLOR)

        grid[0][1] = Knight(DARK_COLOR)
        grid[6][0] = Knight(DARK_COLOR)

        grid[0][2] = Bishop(DARK_COLOR)
        grid[5][0] = Bishop(DARK_COLOR)

        grid[0][7] = Rook(LIGHT_COLOR)
        grid[7][7] = Rook(LIGHT_COLOR)

        grid[0][6] = Knight(LIGHT_COLOR)
        grid[6][6] = Knight(LIGHT_COLOR)

        grid[0][5] = Bishop(LIGHT_COLOR)
        grid[5][5] = Bishop(LIGHT_COLOR)

        for i in range(0, 8):
            grid[i][1] = Pawn(DARK_COLOR)
            grid[i][6] = Pawn(LIGHT_COLOR)
        
        

