import pygame
from classes.piece import Piece
class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.hasMoved = False
    

    def toString(self):
        if self.color == 'white':
            return 'wk'
        else:
            return 'bk'
        

    def can_move(self, src, dest):
        (src_col, src_row) = src
        (dest_col, dest_row) = dest
        
        return ((abs(src_col - dest_col)) < 2 and (abs(src_row - dest_row) < 2))
    
    def can_castle(self, src, dest):
        (src_col, src_row) = src
        (dest_col, dest_row) = dest
        
        if self.color == 'white':
            if (dest_col, dest_row) == (2, 7) or (dest_col, dest_row) == (6, 7):
                return True
        else:
            if (dest_col, dest_row) == (2, 0) or (dest_col, dest_row) == (6, 0):
                return True
        return False
    
    def pass_through(self, src, dest):
        return []