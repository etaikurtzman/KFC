'''
king.py
contains implementation for king class
subclass of piece
4/29
'''
from piece import Piece

class King(Piece):
    """
    A class to represent a king piece
    
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

    can_castle(src, dest):
        Determines if the piece is able to castle or not given a move.
    
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
            The string representation of the piece ('wr' for white king, 'br' 
            for black king).
        """
        # check if the piece is white or black
        if self.color == 'white':
            return 'wk'
        else:
            return 'bk'
        
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
        (destCol, dest_row) = dest
        
        # Check for a valid move within a range of one square horizontally or 
        # vertically
        return ((abs(srcCol - destCol)) < 2 and (abs(srcRow - dest_row) < 2))
    
    def can_castle(self, src, dest):
        """
        Checks if the move is a valid castle move for the king.

        Parameters
        ----------
        src : tuple
            The source coordinates (column, row).
        dest : tuple
            The destination coordinates (column, row).

        Returns
        -------
        bool
            True if the move represents a valid castle move for the king, False
            otherwise.
        """
        (srcCol, srcRow) = src
        (destCol, dest_row) = dest
        
        if self.color == 'white':
            # check if the move is a valid castle position for white
            if (destCol, dest_row) == (2, 7) or (destCol, dest_row) == (6, 7):
                return True
        else:
            # check if the move is a valid castle position for black
            if (destCol, dest_row) == (2, 0) or (destCol, dest_row) == (6, 0):
                return True
        # return false if not valid castle move
        return False
    
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
            The king does not need to check if pieces are in the way therefore
            this function is superfluous.
        """
        return []