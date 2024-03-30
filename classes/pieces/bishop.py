import pygame
from classes.piece import Piece
class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        if self.color == 'white':
            self.image = pygame.image.load('imgs/w_bishop.png')
        else:
            self.image = pygame.image.load('imgs/b_bishop.png')

        self.image = pygame.transform.scale(self.image, (100, 100))


    # Returns true iff move can be valid (given any board state)
    def can_move(self, src, dest):
        (src_col, src_row) = src
        (dest_col, dest_row) = dest
        if src == dest:
            return False
        return abs(src_col - dest_col) == abs(src_row - dest_row)


    # Assumes given move can be valid
    def pass_through(self, src, dest):
        (src_col, src_row) = src
        (dest_col, dest_row) = dest

        col_inc = (src_col - dest_col) / abs(src_col - dest_col)
        row_inc = (src_row - dest_row) / abs(src_row - dest_row)

        squares_passed = []

        i = src_col + col_inc
        j = src_row + row_inc
        for _ in range(src_col + 1, dest_col):
            squares_passed.append((i, j))
            i += col_inc
            j += row_inc




        # if (src_col != dest_col):
        #     start = min(src_col, dest_col)
        #     end = max(src_col, dest_col)
        #     return [(i, dest_row) for i in range(start + 1, end)]
        # else:
        #     start = min(src_row, dest_row)
        #     end = max(src_row, dest_row)
        #     return [(dest_col, j) for j in range(start + 1, end)]
