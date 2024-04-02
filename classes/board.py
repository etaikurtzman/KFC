import pygame
import threading
from classes.pieces.bishop import Bishop
from classes.pieces.rook import Rook
from classes.pieces.knight import Knight
from classes.pieces.king import King
from classes.pieces.pawn import Pawn
from classes.pieces.queen import Queen

PIECE_LIGHT_COLOR = 'white'
PIECE_DARK_COLOR  = 'black'


class Board:
    def __init__(self, screen):
        self.screen = screen
        self.length = 8
        self.pixelLength = 800
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.gridLocks =  [[threading.Lock for _ in range(8)] for _ in range(8)]
        
        self.grid[0][0] = Rook(PIECE_DARK_COLOR)
        self.grid[7][0] = Rook(PIECE_DARK_COLOR)

        self.grid[1][0] = Knight(PIECE_DARK_COLOR)
        self.grid[6][0] = Knight(PIECE_DARK_COLOR)

        self.grid[2][0] = Bishop(PIECE_DARK_COLOR)
        self.grid[5][0] = Bishop(PIECE_DARK_COLOR)

        self.grid[3][0] = King(PIECE_DARK_COLOR)
        self.grid[4][0] = Queen(PIECE_DARK_COLOR)
        
        self.grid[0][7] = Rook(PIECE_LIGHT_COLOR)
        self.grid[7][7] = Rook(PIECE_LIGHT_COLOR)

        self.grid[1][7] = Knight(PIECE_LIGHT_COLOR)
        self.grid[6][7] = Knight(PIECE_LIGHT_COLOR)

        self.grid[2][7] = Bishop(PIECE_LIGHT_COLOR)
        self.grid[5][7] = Bishop(PIECE_LIGHT_COLOR)

        self.grid[3][7] = King(PIECE_LIGHT_COLOR)
        self.grid[4][7] = Queen(PIECE_LIGHT_COLOR)

        for i in range(0, 8):
            self.grid[i][1] = Pawn(PIECE_DARK_COLOR)
            self.grid[i][6] = Pawn(PIECE_LIGHT_COLOR)
        

    def move(self, src, dest):
        (src_col, src_row) = src
        (dest_col, dest_row) = dest
        if not self.grid[src_col][src_row]:
            return False # no piece at origin
        if isinstance(self.grid[src_col][src_row], Pawn):
            if self.grid[dest_col][dest_row]:
                if self.grid[dest_col][dest_row].color != self.grid[src_col][src_row].color:
                    if self.grid[src_col][src_row].can_capture(src, dest):
                        self.grid[dest_col][dest_row] = self.grid[src_col][src_row]
                        self.grid[src_col][src_row] = None
                    return
                else:
                    return False

    
        if (self.grid[src_col][src_row].can_move(src, dest)):
            passed = self.grid[src_col][src_row].pass_through(src, dest)
            for (i,j) in passed:
                if self.grid[i][j]:
                    return False # piece in the way
        else:
            return False
        if self.grid[dest_col][dest_row]:
            if self.grid[dest_col][dest_row].color == self.grid[src_col][src_row].color:
                return False # friendly fire
        
        self.grid[dest_col][dest_row] = self.grid[src_col][src_row]
        self.grid[src_col][src_row] = None
        
        
        
    def draw(self):
        for i in range(self.length):
            for j in range(self.length):
                if self.grid[i][j]:
                    self.screen.blit(self.grid[i][j].image, ((i * (self.pixelLength // self.length)), (j * (self.pixelLength // self.length))))