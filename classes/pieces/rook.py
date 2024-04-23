import pygame
from classes.piece import Piece
class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.hasMoved = False
        self.cooldown = 4.0

    def toString(self):
        if self.color == 'white':
            return 'wr'
        else:
            return 'br'
        

    # Returns true iff move can be valid (given any board state)
    def can_move(self, src, dest):
        (src_col, src_row) = src
        (dest_col, dest_row) = dest

        return (src_col == dest_col or src_row == dest_row)

    # Assumes given move can be valid
    def pass_through(self, src, dest):
        (src_col, src_row) = src
        (dest_col, dest_row) = dest
        
        if (src_col != dest_col):
            start = min(src_col, dest_col)
            end = max(src_col, dest_col)
            return [(i, dest_row) for i in range(start + 1, end)]
        else:
            start = min(src_row, dest_row)
            end = max(src_row, dest_row)
            return [(dest_col, j) for j in range(start + 1, end)]

