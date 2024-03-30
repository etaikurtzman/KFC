import pygame
from classes.piece import Piece

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        if self.color == 'white':
            self.image = pygame.image.load('imgs/w_pawn.png')
        else:
            self.image = pygame.image.load('imgs/b_pawn.png')

        self.image = pygame.transform.scale(self.image, (100, 100))