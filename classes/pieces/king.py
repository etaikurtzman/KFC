import pygame
from classes.piece import Piece
class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        if self.color == 'white':
            self.image = pygame.image.load('imgs/w_king.png')
        else:
            self.image = pygame.image.load('imgs/b_king.png')

        self.image = pygame.transform.scale(self.image, (100, 100))
    

    def toString(self):
        if self.color == 'white':
            return 'wk'
        else:
            return 'bk'
        

    def can_move(self, src, dest):
        (src_col, src_row) = src
        (dest_col, dest_row) = dest
        if src == dest:
            return False
        return ((abs(src_col - dest_col)) < 2 and (abs(src_row - dest_row) < 2))
    
    def pass_through(self, src, dest):
        return []