import pygame
from classes.piece import Piece
class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)

    def toString(self):
        if self.color == 'white':
            return 'wq'
        else:
            return 'bq'

    
    def can_move(self, src, dest):
        (src_col, src_row) = src
        (dest_col, dest_row) = dest

        if src == dest:
            return False
        return (abs(src_col - dest_col) == abs(src_row - dest_row)) or (src_col == dest_col or src_row == dest_row)
    
    def pass_through(self, src, dest):
        (src_col, src_row) = src
        (dest_col, dest_row) = dest

        if (src_col != dest_col and src_row == dest_row):
            start = min(src_col, dest_col)
            end = max(src_col, dest_col)
            return [(i, dest_row) for i in range(start + 1, end)]
        elif (src_row != dest_row and src_col == dest_col):
            start = min(src_row, dest_row)
            end = max(src_row, dest_row)
            return [(dest_col, j) for j in range(start + 1, end)]
        else:
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