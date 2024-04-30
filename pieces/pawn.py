'''
pawn.py
contains implementation for pawn class
subclass of piece
4/29
'''
from piece import Piece

class Pawn(Piece):
    """
    A class to represent a pawn piece

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

    can_capture(src, dest):
        Determines if the piece can capture another piece or not.
    
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
            The string representation of the piece ('wr' for white pawn, 'br' 
            for black pawn).
        """
        # check if the piece is white or black
        if self.color == 'white':
            return 'wp'
        else:
            return 'bp'

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
        
        # Returns true iff move can be valid (given any board state)
        # For pawn, this function returns true only if the pawn is not 
        # capturing, but moving forward. There is a separate can_capture method
        if self.color == 'white':
            if srcRow == 6:
                # If the white pawn is in its starting position (row 6), it can 
                # move either one or two steps forward, but cannot capture.
                return (destRow == 5 or destRow == 4) and (srcCol == destCol)
            else:
                # If the white pawn has already moved from its starting 
                # position, it can only move one step forward, not capturing.
                return (destRow == srcRow - 1) and (srcCol == destCol)
        else:
            if srcRow == 1:
                # If the black pawn is in its starting position (row 6), it can 
                # move either one or two steps forward, but cannot capture.
                return (destRow == 2 or destRow == 3) and (srcCol == destCol)
            else:
                # If the black pawn has already moved from its starting 
                # position, it can only move one step forward, not capturing.
                return (destRow == srcRow + 1) and (srcCol == destCol)
            
    def can_capture(self, src, dest):
        """
        Check if the piece can capture an opponent's piece.

        Parameters
        ----------
        src : tuple
            The source coordinates (column, row).
        dest : tuple
            The destination coordinates (column, row).

        Returns
        -------
        bool
            True if the piece can capture the opponent's piece at the 
            destination, False otherwise.
        """
        (srcCol, srcRow) = src
        (destCol, destRow) = dest

        # Check if destination is adjacent to source column-wise
        if destCol == srcCol + 1 or destCol == srcCol - 1:
            # White piece captures by moving one row up
            if self.color == 'white':
                return (destRow == srcRow - 1)
            # Black piece captures by moving one row dow
            else:
                return (destRow == srcRow + 1)
        # If destination is not adjacent column-wise, capture is not possible
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
        list of tuple
            Intermediate positions between source and destination.
        """
        (srcCol, srcRow) = src
        (destCol, destRow) = dest

        squares_passed = []

        # Check if the destination is two rows ahead of the source
        if   destRow == srcRow + 2:
            # Add the position between source and destination
            squares_passed.append((srcCol, srcRow + 1))
        # Check if the destination is two rows behind the source
        elif destRow == srcRow - 2:
            squares_passed.append((srcCol, srcRow - 1))
        
        return squares_passed