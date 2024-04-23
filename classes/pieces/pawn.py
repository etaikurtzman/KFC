import pygame
from classes.piece import Piece

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.cooldown = 1.0

    def toString(self):
        if self.color == 'white':
            return 'wp'
        else:
            return 'bp'


    # Returns true iff move can be valid (given any board state)
    # For pawn, this function returns true only if the pawn is not capturing,
    # but moving forward. There is a separate can_capture method
    def can_move(self, src, dest):
        (src_col, src_row) = src
        (dest_col, dest_row) = dest
        
        if self.color == 'white':
            if src_row == 6:
                return (dest_row == 5 or dest_row == 4) and (src_col == dest_col)
            else:
                return (dest_row == src_row - 1) and (src_col == dest_col)
        else:
            if src_row == 1:
                return (dest_row == 2 or dest_row == 3) and (src_col == dest_col)
            else:
                return (dest_row == src_row + 1) and (src_col == dest_col)
            
            

    def can_capture(self, src, dest):
        (src_col, src_row) = src
        (dest_col, dest_row) = dest
        if src == dest:
            return False

        if dest_col == src_col + 1 or dest_col == src_col - 1:
            if self.color == 'white':
                return (dest_row == src_row - 1)
            else:
                return (dest_row == src_row + 1)

        return False


    # Assumes given move can be valid
    def pass_through(self, src, dest):
        (src_col, src_row) = src
        (dest_col, dest_row) = dest

        squares_passed = []

        if   dest_row == src_row + 2:
            squares_passed.append((src_col, src_row + 1))
        elif dest_row == src_row - 2:
            squares_passed.append((src_col, src_row - 1))
        
        return squares_passed