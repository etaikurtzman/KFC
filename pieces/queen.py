'''
queen.py
contains implementation for queen class
subclass of piece
4/29
'''
from piece import Piece

class Queen(Piece):
    """
    A class to represent a queen piece

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
            The string representation of the piece ('wr' for white queen, 'br' 
            for black queen).
        """
        # check if the piece is white or black
        if self.color == 'white':
            return 'wq'
        else:
            return 'bq'

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
        return (abs(srcCol - destCol) == abs(srcRow - destRow)) or \
               (srcCol == destCol or srcRow == destRow)
    
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

        # if the move is horizontal
        if (srcCol != destCol and srcRow == destRow):
            start = min(srcCol, destCol)
            end = max(srcCol, destCol)
            return [(i, destRow) for i in range(start + 1, end)]
        # if the move is vertical
        elif (srcRow != destRow and srcCol == destCol):
            start = min(srcRow, destRow)
            end = max(srcRow, destRow)
            return [(destCol, j) for j in range(start + 1, end)]
        else:
            # if the move is diagonal
            col_inc = (destCol - srcCol) // abs(srcCol - destCol)
            row_inc = (destRow - srcRow) // abs(srcRow - destRow)

            squares_passed = []

            # generate list of coordinates from start to end
            i = srcCol + col_inc
            j = srcRow + row_inc
            for _ in range(abs(srcCol - destCol) - 1):
                squares_passed.append((i, j))
                i += col_inc
                j += row_inc
            
            return squares_passed