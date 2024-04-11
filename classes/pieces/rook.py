import pygame
from classes.piece import Piece
class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        if self.color == 'white':
            self.image = pygame.image.load('imgs/w_rook.png')
        else:
            self.image = pygame.image.load('imgs/b_rook.png')

        self.image = pygame.transform.scale(self.image, (100, 100))
        
        # code for experimenting
        #self.rect = self.image.get_rect()
        #self.topleft = (x, y)
        #self.dragging = False
    
    #def update(self):
    #    if self.dragging:
    #        self.rect.center = pygame.mouse.get_pos()
    
    #def draw(self, screen):
    #    screen.blit(self.image, self.rect.topleft)


    def toString(self):
        if self.color == 'white':
            return 'wr'
        else:
            return 'br'
        

    # Returns true iff move can be valid (given any board state)
    def can_move(self, src, dest):
        (src_col, src_row) = src
        (dest_col, dest_row) = dest
        if src == dest:
            return False
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

