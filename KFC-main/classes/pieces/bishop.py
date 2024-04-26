import pygame
from classes.piece import Piece
class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)

    def toString(self):
        if self.color == 'white':
            return 'wb'
        else:
            return 'bb'


    # Returns true iff move can be valid (given any board state)
    def can_move(self, src, dest):
        (src_col, src_row) = src
        (dest_col, dest_row) = dest
        return abs(src_col - dest_col) == abs(src_row - dest_row)


    # Assumes given move can be valid
    def pass_through(self, src, dest):
        (src_col, src_row) = src
        (dest_col, dest_row) = dest

        col_inc = (dest_col - src_col) // abs(src_col - dest_col)
        row_inc = (dest_row - src_row) // abs(src_row - dest_row)

        squares_passed = []

        i = src_col + col_inc
        j = src_row + row_inc
        for _ in range(abs(src_col - dest_col) - 1):
            squares_passed.append((i, j))
            i += col_inc
            j += row_inc
        
        return squares_passed


