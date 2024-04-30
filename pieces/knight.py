'''
knight.py
contains implementation for knight class
subclass of piece
4/29
'''
from piece import Piece

class Knight(Piece):
    """
    A class to represent a knight piece

    Members
    -------
    hasMoved: bool
        whether or not this piece has moved during the game.

    Functions
    ---------
    to_string():
        get the string representation of the piece
    
    can_move(src, dest):
        Determines if the piece can move to certain square or not.
    
    pass_through(src, dest):
        Generate a list of squares the piece will traverse while moving. 

    """
    def __init__(self, color):
        super().__init__(color)

    def to_string(self):
        """
        Get the string representation of the piece.

        Returns
        -------
        str
            The string representation of the piece ('wr' for white knight, 'br'
            for black knight).
        """
        # check if the piece is white or black
        if self.color == 'white':
            return 'wn'
        else:
            return 'bn'

    def can_move(self, src, dest):
        """
        Check if the piece can move from source to destination.

        Parameters
        ----------
        src : tuple
            The source coordinates (column, row).
        dest : tuple
            The destination coordinates (column, row).

        Returns
        -------
        bool
            True if the move is valid (horizontal or vertical), False otherwise.
        """
        (srcCol, srcRow) = src
        (destCol, destRow) = dest
        # Check if knight has moved 2 squares horizontally and 1 square 
        # vertically.
        return (abs(srcCol - destCol) == 2 and abs(srcRow - destRow) == 1) or \
               (abs(srcCol - destCol) == 1 and abs(srcRow - destRow) == 2)
               # Check if knight has moved 2 squares vertically and 1 square
               # horizontally.

    def pass_through(self, src, dest):
        """
        Generates intermediate positions for a straight move from source to 
        destination.

        Parameters
        ----------
        src : tuple
            The source coordinates (column, row).
        dest : tuple
            The destination coordinates (column, row).

        Returns
        -------
        empty list
            The knight does not need to check if pieces are in the way therefore
            this function is superfluous.
        """
        return []