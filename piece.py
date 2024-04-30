'''
piece.py
contains implementation for piece class
superclass that represents each piece on the board
4/29
'''

class Piece:
    """
    A class to represent a piece on the chess board

    Members
    -------
    color: str
        the color of the piece object ('white' or 'black')

    lastMoved: float
        the last time this piece was moved

    cooldown: float
        represents this piece's cooldown, in seconds

    Functions
    ---------
    udpate_timer(time):
        updates this player's last move time
    
    moved_recently(time):
        determine whether this piece is on cooldown
    
    get_cooldown():
        gets this piece's cooldown time

    """
    def __init__(self, color):
        self.color = color
        self.lastMoved = None
        self.cooldown = 3.0

    def update_timer(self, time):
        """
        Updates this player's lastMoved time

        Parameters
        ----------
        time : float
            The time when this piece was last moved.
        """
        self.lastMoved = time

    def moved_recently(self, time):
        """
        Returns whether or not this piece is on cooldown, based on the given
        time.

        Parameters
        ----------
        time : float
            Time to base this piece's cooldown on

        Returns
        -------
        bool
        """
        if self.lastMoved:
            return time - self.lastMoved < self.cooldown
        return False
    
    def get_cooldown(self):
        """
        Returns this piece's cooldown time.

        Returns
        -------
        float
        """
        return self.cooldown