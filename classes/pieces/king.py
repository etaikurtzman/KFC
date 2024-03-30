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