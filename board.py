'''
board.py
contains implementation for board class
represents chess board and handles logic for move validity
4/29
'''

# Imported pieces
from pieces.bishop import Bishop
from pieces.rook import Rook
from pieces.knight import Knight
from pieces.king import King
from pieces.pawn import Pawn
from pieces.queen import Queen

# imported modules
import time
from threading import Lock

# Length of the grid (number of squares)
LENGTH = 8

class Board:
    """
    A class to represent a chess board and chess game logic

    Members
    -------
    grid: list(list(Piece))
        the chess board indexed by col, row where (0,0) is the top left
        an entry of None represents and empty square

    gridLocks: list(list(Lock))
        a lock corresponding to each square in the board to grant exclusive
        access to that square

    startTime: float
        represents the time, in seconds that the game began
    
    self.winner: str
        represents the player that won by the color of their pieces

    self.currTime: float
        represent the last time a move was attempted

    Functions
    ---------
    start_timer():
        starts game timer and initializes startTime
    
    init_pieces():
        initializes pieces on board
    
    move(src, dest, playerColor): str
        determines if a move is valid
    
    click(clickCoordinates, playerColor): bool
        checks if a player clicks one of their pieces

    grid_to_string(): str
        returns a string representation of the board
    
    get_cooldown_string(coord): str
        returns the string of a piece's cool down at a given index

    pawn_capture(src, dest, toMove, playerColor): boolean
        determines if a pawn at a source can capture a piece at the destination
        performs the capture and returns whether a capture was performed

    promote(dest, toMove, playerColor):
        promotes if a piece to be moved is a pawn and moving to a back row

    acquire_gridlocks(coordinates): bool, list(bool)
        acquires the locks at every square in a list of coordinates
    
    is_trying_to_castle(toMove, src, dest): bool
        determines if a king is attempting to castle
    
    castle(self, src, dest, rookSrc, rookDest, lockingSquares,
               mustBeEmptySquares, playerColor): 
               determines if a castle is possible and performs it if so
    
    """
    def __init__(self):
        l = LENGTH
        self.grid = [[None for _ in range(l)] for _ in range(l)]
        self.init_pieces()

        self.gridLocks = [[Lock() for _ in range(l)] for _ in range(l)]
        

        self.startTime = None
        self.winner = None
        self.currTime = None
    
    def start_timer(self):
        '''
            Starts the board timer

            Parameters:

            Returns: the start time in seconds (float)
                    
        '''
        self.startTime = time.perf_counter()
        return self.start_timer
        
    def init_pieces(self):
        '''
            Populates the board with pieces

            Parameters:

            Returns: None
                    
        '''
        self.grid[0][0] = Rook("black")
        self.grid[7][0] = Rook("black")

        self.grid[1][0] = Knight("black")
        self.grid[6][0] = Knight("black")

        self.grid[2][0] = Bishop("black")
        self.grid[5][0] = Bishop("black")

        self.grid[3][0] = Queen("black")
        self.grid[4][0] = King("black")
        
        self.grid[0][7] = Rook("white")
        self.grid[7][7] = Rook("white")

        self.grid[1][7] = Knight("white")
        self.grid[6][7] = Knight("white")

        self.grid[2][7] = Bishop("white")
        self.grid[5][7] = Bishop("white")

        self.grid[3][7] = Queen("white")
        self.grid[4][7] = King("white")

        for i in range(0, LENGTH):
            self.grid[i][1] = Pawn("black")
            self.grid[i][6] = Pawn("white")
        return


    def move(self, src, dest, playerColor):
        '''
            Determines if a move is valid, and updates the board accordingly
            if so

            Parameters:
                src: 
                    a tuple of ints representing the source of the attempted
                    move
                
                dest:  
                    a tuple of ints representing the destination of the
                    attempted move
                
                playerColor (str):
                    the color of the pieces of the player 
                    attempting the move

            Returns: the string representation of the piece in the destination
            if the move wass succesful succesful, None otherwise
                    
        '''

        # check if same square got clicked and unclicked
        if src == dest:
            return None

        (srcCol, srcRow) = src
        (destCol, destRow) = dest

        # grab the locks associated with the source and destination squares
        srcLock = self.gridLocks[srcCol][srcRow].acquire(timeout=1)
        destLock = self.gridLocks[destCol][destRow].acquire(timeout=1)

        if srcLock and destLock:
            try:
                # If trying to move a piece from an empty square
                if not self.grid[srcCol][srcRow]:
                    return None # no piece at origin
                
                toMove = self.grid[srcCol][srcRow]

                # ensure player is moving their own piece
                if playerColor != toMove.color:
                    return None
                
                # checks if the piece is cooling down
                self.currTime = time.perf_counter()
                if toMove.moved_recently(self.currTime):
                    return None

                # checking if destination is the king, if so winner is set
                possible_winner = None
                if isinstance(self.grid[destCol][destRow], King):
                    if self.grid[destCol][destRow].color == "white":
                        possible_winner = "black"
                    else:
                        possible_winner = "white"

                # If trying to move a pawn
                if isinstance(toMove, Pawn):
                    if self.grid[destCol][destRow]:
                        if self.pawn_capture(src, dest, toMove, playerColor):
                            self.winner = possible_winner
                            return self.grid[destCol][destRow].to_string()
                        else:
                            return None
                
                # If trying to move a king and that king can castle
                if self.is_trying_to_castle(toMove, src, dest):

                    # White Queenside Castling
                    if playerColor == "white" and dest == (2, 7):      
                        self.castle(src, dest, (0, 7), (3, 7),
                            [(1,7), (3,7), (0,7)], [(1,7), (2,7), (3,7)],
                            playerColor)
                    # White Kingside Castling
                    elif playerColor == "white" and dest == (6, 7):
                        self.castle(src, dest, (7, 7), (5, 7),
                            [(5,7), (7,7)], [(5, 7), (6, 7)],playerColor)

                    # Black Queenside Castling
                    elif playerColor == "black" and dest == (2, 0):
                        self.castle(src, dest, (0, 0), (3, 0),
                            [(1,0), (3,0), (0, 0)], [(1, 0), (2, 0), (3, 0)],
                            playerColor)
                   
                    # Black Kingside Castling
                    elif playerColor == "black" and dest == (6, 0):
                        self.castle(src, dest, (7, 0), (5, 0), [(5,0), (7, 0)],
                        [(5, 0), (6, 0)], playerColor)
                       
                    return self.grid[destCol][destRow].to_string()

                # check if there's a piece in the way
                if (toMove.can_move(src, dest)):
                    passed = toMove.pass_through(src, dest)
                    for (i,j) in passed:
                        if self.grid[i][j]:
                            return None # piece in the way
                else:
                    return None
                
                # check if the destination is a piece of the same color
                if self.grid[destCol][destRow]:
                    if self.grid[destCol][destRow].color == toMove.color:
                        return None # friendly fire
                
                # Successful move
                self.grid[destCol][destRow] = toMove
                self.grid[srcCol][srcRow] = None
                self.grid[destCol][destRow].update_timer(time.perf_counter())
                self.promote(dest, toMove, playerColor)
                self.winner = possible_winner
                
                # if the king or rook have moved
                if isinstance(self.grid[destCol][destRow], King) or \
                  isinstance(self.grid[destCol][destRow], Rook):
                  self.grid[destCol][destRow].hasMoved = True
                
                return self.grid[destCol][destRow].to_string()
            
            finally:
                # release locks after move has been made
                self.gridLocks[srcCol][srcRow].release()
                self.gridLocks[destCol][destRow].release()
        else:
            # give back locks if something went wrong
            if srcLock:
                    self.gridLocks[srcCol][srcRow].release()
            if destLock:
                self.gridLocks[destCol][destRow].release()
            return None
    
    def click(self, clickCoordinates, playerColor):
        '''
            Determines of a clicked square contains a piece belonging to a 
            certain player

            Parameters:
                clickCoordinates: 
                    a tuple of ints representing the click
                
                playerColor (str):
                    the color of the pieces of the player clicking

            Returns: true if the clicked squared contains a piece belonging
            to the player who clicked, false otherwise
                    
        '''
        (clickCol, clickRow) = clickCoordinates
        # if a piece exists at the destination
        if self.grid[clickCol][clickRow]:
            # if there is a piece of the same color
            if self.grid[clickCol][clickRow].color == playerColor:
                return True
        return False
        
    def grid_to_string(self):  
        '''
            Returns a string representation of the board. The string is 
            seperated by commas such that between each comma represents what
            a given cell contains. The string is ordered in column major order
            A period represents an empty square

            Parameters:

            Returns: s, the string representation of the board
                    
        '''   
        s = ""
        for i in range(LENGTH):
            for j in range(LENGTH):
                if self.grid[i][j]:
                    # if there is a piece append the string name
                    s += (self.grid[i][j].to_string() + ",")
                else:
                    # if there isn't a piece add a period
                    s += ".,"
        s = s[:-1]
        # if there is a winner append string to the end. 
        if self.winner:
            return self.winner + ":" + s
        else:
            return s

    def get_cooldown_string(self, coord):
        '''
            Gets a string reprsenting the cooldown time of a piece at a given
            coordinate

            Parameters:
                coord: 
                    a tuple of ints representing the coordinates of the piece

            Returns: a string of the piece's cooldown time
                    
        '''
        col, row = coord
        return str(self.grid[col][row].get_cooldown())
        
    def pawn_capture(self, src, dest, toMove, playerColor):
        '''
            Handles the logic of a pawn being dragged to a square with another
            piece. Performs move and promotes pawn if applicable

            Parameters:
                src: 
                    a tuple of ints representing the source of the attempted
                    move
                
                dest:  
                    a tuple of ints representing the destination of the
                    attempted move
                
                toMove (Piece): the pawn that is being attemped to move
                
                playerColor (str):
                    the color of the pieces of the player 
                    attempting the capture

            Returns: True if the move was succesful, False otherwise
                    
        '''
        # returns if the pawn can capture the destination
        (srcCol, srcRow) = src
        (destCol, destRow) = dest
        if self.grid[destCol][destRow].color != toMove.color:
            if toMove.can_capture(src, dest):
                self.grid[destCol][destRow] = toMove
                self.grid[destCol][destRow].update_timer(self.currTime)
                self.grid[srcCol][srcRow] = None
                self.promote(dest, toMove, playerColor)
                return True
        return False

    def promote(self, dest, toMove, playerColor):
        '''
            Checks if a piece being moved needs to be promoted, and promotes it
            to a queen if applicable.

            Parameters:
                dest:  
                    a tuple of ints representing the destination of the
                    attempted move
                    
                toMove (Piece): the pawn that is being attemped to move
                
                playerColor (str):
                    the color of the pieces of the player 
                    attempting the move

            Returns: None
                    
        '''
        (destCol, destRow) = dest
        # if the pawn has reached the end of the board promote it to a queen
        if isinstance(toMove, Pawn):
            if destRow == 0 or destRow == 7:
                self.grid[destCol][destRow] = Queen(playerColor)
                self.grid[destCol][destRow].update_timer(self.currTime)
        return


    def acquire_gridlocks(self, coordinates):
        '''
            Takes a list of coordinates in the locking array and acquires the 
            associated locks.
            
            Parameters:
                coordinates:
                    a list of (col, row) tuples associated with the 

            Returns:
                A tuple (success, locks)
                
                locks is a list of booleans reprenting whether or not each
                associated lock in coordinates was successfully acquired

                success is a boolean which is True iff every boolean in locks
                is True
                    
        '''
        locks = []
        success = True
        for coord in coordinates:
            # get the row and col and acquire that lock
            (col, row) = coord
            lock = self.gridLocks[col][row].acquire(timeout=1)
            if not lock:
                success = False
            locks.append(lock)
        return success, locks

    def is_trying_to_castle(self, toMove, src, dest):
        '''
            Takes a piece, a source square, and a destination square. Returns
            True iff that piece is a King which is trying to castle
            
            Parameters:
                toMove:
                    A piece object associated with the attempted move
                src:
                    The source square from which the piece is moving (col, row)
                dest:
                    The dest square to which the piece is moving (col, row)

            Returns:
                True iff that piece is a King which is trying to castle.
                False otherwise
                    
        '''
        # if the piece is a king, hasn't moved and can castle
        return isinstance(toMove, King)  \
               and (not toMove.hasMoved) \
               and toMove.can_castle(src, dest)

    def castle(self, src, dest, rookSrc, rookDest, lockingSquares,
               mustBeEmptySquares, playerColor):
        '''
            Executes a castling move.
            
            Parameters:
                src:
                    King's source square
                dest:
                    King's destination square
                rookSrc:
                    Rook's source square
                rookDest:
                    Rook's destination square
                lockingSquares:
                    A list of squares which must be locked during the move
                mustBeEmptySquares:
                    A list of squares which must be empty prior to the move
                playerColor:
                    The color of the player making the move

            Returns: N/A (void)
                
                    
        '''
        (srcCol, srcRow)   = src
        (destCol, destRow) = dest
        (rookSrcCol, rookSrcRow) = rookSrc
        (rookDestCol, rookDestRow) = rookDest
        success, locks = self.acquire_gridlocks(lockingSquares)
        if success:
            try:
                # squaresAreEmpty stays True if every square in
                # mustBeEmptySquares is empty
                squaresAreEmpty = True
                for square in mustBeEmptySquares:
                    (squareCol, squareRow) = square
                    squaresAreEmpty = squaresAreEmpty \
                                  and (not self.grid[squareCol][squareRow])
                # if the piece trying to castle with is a rook of the same color
                rookPiece = self.grid[rookSrcCol][rookSrcRow]
                rookIsEligible = isinstance(rookPiece, Rook)    \
                             and rookPiece.color == playerColor \
                             and (not rookPiece.hasMoved)
                
                
                if squaresAreEmpty and rookIsEligible:
                # move king
                    self.grid[destCol][destRow] = self.grid[srcCol][srcRow]
                    self.grid[destCol][destRow].hasMoved = True
                    self.grid[srcCol][srcRow] = None
                    # move rook
                    self.grid[rookDestCol][rookDestRow] = \
                        self.grid[rookSrcCol][rookSrcRow]
                    self.grid[rookDestCol][rookDestRow].hasMoved = True
                    self.grid[rookSrcCol][rookSrcRow] = None
            finally:
                # release the destination square locks
                for lockingSquare in lockingSquares:
                    (lsCol, lsRow) = lockingSquare
                    self.gridLocks[lsCol][lsRow].release()
                    
        else:
            # release all locks
            for i in range(len(locks)):
                if locks[i]:
                    (lsCol, lsRow) = lockingSquares[i]
                    self.gridLocks[lsCol][lsRow].release()
