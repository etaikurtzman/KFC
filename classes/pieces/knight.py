import pygame
from classes.piece import Piece

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        if self.color == 'white':
            self.image = pygame.image.load('imgs/w_knight.png')
        else:
            self.image = pygame.image.load('imgs/b_knight.png')

        self.image = pygame.transform.scale(self.image, (100, 100))
    

    def toString(self):
        if self.color == 'white':
            return 'wn'
        else:
            return 'bn'


    # Returns true iff move can be valid (given any board state)
    def can_move(self, src, dest):
        (src_col, src_row) = src
        (dest_col, dest_row) = dest
        return (abs(src_col - dest_col) == 2 and abs(src_row - dest_row) == 1) or \
               (abs(src_col - dest_col) == 1 and abs(src_row - dest_row) == 2)


    # Assumes given move can be valid
    def pass_through(self, src, dest):
        return []