'''
rook.py
contains implementation for rook class
subclass of piece
4/29
'''

from piece import Piece

class Rook(Piece):
    """
    A class to represent a rook piece

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
        self.hasMoved = False

    def to_string(self):
        """
        Get the string representation of the piece.

        Returns
        -------
        str
            The string representation of the piece ('wr' for white rook, 'br' 
            for black rook).
        """
        # check if the piece is white or black
        if self.color == 'white':
            return 'wr'
        else:
            return 'br'
        

    
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

        # check if the move is valid or not
        return (srcCol == destCol or srcRow == destRow)

    
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
        list of tuple
            Intermediate positions between source and destination.
        """
        # Assumes given move can be valid
        (srcCol, srcRow) = src
        (destCol, destRow) = dest
        
        # if moving horizontally
        if (srcCol != destCol):
            # get start and end positions
            start = min(srcCol, destCol)
            end = max(srcCol, destCol)
            # return list of all squares between start and end
            return [(i, destRow) for i in range(start + 1, end)]
        # if moving vertically
        else:
            start = min(srcRow, destRow)
            end = max(srcRow, destRow)
            return [(destCol, j) for j in range(start + 1, end)]

