import pygame
import threading
from classes.pieces.bishop import Bishop
from classes.pieces.rook import Rook
from classes.pieces.knight import Knight
from classes.pieces.king import King
from classes.pieces.pawn import Pawn
from classes.pieces.queen import Queen
import time

PIECE_LIGHT_COLOR = 'white'
PIECE_DARK_COLOR  = 'black'


class Board:
    def __init__(self):
        self.length = 8
        self.winner = None

        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.gridLocks =  [[threading.Lock() for _ in range(8)] for _ in range(8)]
        
        self.grid[0][0] = Rook(PIECE_DARK_COLOR)
        self.grid[7][0] = Rook(PIECE_DARK_COLOR)

        self.grid[1][0] = Knight(PIECE_DARK_COLOR)
        self.grid[6][0] = Knight(PIECE_DARK_COLOR)

        self.grid[2][0] = Bishop(PIECE_DARK_COLOR)
        self.grid[5][0] = Bishop(PIECE_DARK_COLOR)

        self.grid[3][0] = Queen(PIECE_DARK_COLOR)
        self.grid[4][0] = King(PIECE_DARK_COLOR)
        
        self.grid[0][7] = Rook(PIECE_LIGHT_COLOR)
        self.grid[7][7] = Rook(PIECE_LIGHT_COLOR)

        self.grid[1][7] = Knight(PIECE_LIGHT_COLOR)
        self.grid[6][7] = Knight(PIECE_LIGHT_COLOR)

        self.grid[2][7] = Bishop(PIECE_LIGHT_COLOR)
        self.grid[5][7] = Bishop(PIECE_LIGHT_COLOR)

        self.grid[3][7] = Queen(PIECE_LIGHT_COLOR)
        self.grid[4][7] = King(PIECE_LIGHT_COLOR)

        for i in range(0, 8):
            self.grid[i][1] = Pawn(PIECE_DARK_COLOR)
            self.grid[i][6] = Pawn(PIECE_LIGHT_COLOR)

        self.startTime = None
        
        self.captured = []
    
    def start_timer(self):
        self.startTime = time.perf_counter()
        

    def move(self, src, dest, playerColor):
        if src == dest:
            return False

        (src_col, src_row) = src
        (dest_col, dest_row) = dest

        src_lock = self.gridLocks[src_col][src_row].acquire(timeout=1)
        dest_lock = self.gridLocks[dest_col][dest_row].acquire(timeout=1)

        if src_lock and dest_lock:
            try:
                # If trying to move a piece from an empty square
                if not self.grid[src_col][src_row]:
                    return False # no piece at origin
                

                # ensure player is moving their own piece
                if playerColor != self.grid[src_col][src_row].color:
                    return False
                
                
                
                # checks if the piece moved recently
                # print(time.perf_counter())
                if self.grid[src_col][src_row].movedRecently(time.perf_counter()):
                    return False
                # print("hello")
                # checking if destination is the king, if so winner is set
                possible_winner = None
                if isinstance(self.grid[dest_col][dest_row], King):
                    if self.grid[dest_col][dest_row].color == PIECE_LIGHT_COLOR:
                        possible_winner = PIECE_DARK_COLOR
                    else:
                        possible_winner = PIECE_LIGHT_COLOR

                # If trying to move a pawn
                if isinstance(self.grid[src_col][src_row], Pawn):
                    if self.grid[dest_col][dest_row]:
                        if self.grid[dest_col][dest_row].color != self.grid[src_col][src_row].color:
                            if self.grid[src_col][src_row].can_capture(src, dest):
                                if dest_row == 0 or dest_row == 7:
                                    self.grid[dest_col][dest_row] = Queen(playerColor)
                                    self.grid[dest_col][dest_row].updateTimer(time.perf_counter()) # Successful pawn move (promotion to queen)
                                else:
                                    self.grid[dest_col][dest_row] = self.grid[src_col][src_row]
                                    self.grid[dest_col][dest_row].updateTimer(time.perf_counter())  # Successful pawn move
                                self.grid[src_col][src_row] = None
                                self.winner = possible_winner
                                self.captured.append(self.grid[dest_col][dest_row].toString())
                            return True
                        else:
                            return False
                
                # If trying to move a king
                if isinstance(self.grid[src_col][src_row], King):
                    # if trying to castle
                    if (not self.grid[src_col][src_row].hasMoved) and self.grid[src_col][src_row].can_castle(src, dest):
                        # check player color
                        if playerColor == PIECE_LIGHT_COLOR:
                            # check queenside castle for white is valid
                            if dest == (2, 7) and self.gridLocks[1][7].acquire(timeout=1) and self.gridLocks[3][7].acquire(timeout=1) and self.gridLocks[0][7].acquire(timeout=1):
                                try:
                                    if (not self.grid[1][7]) and (not self.grid[2][7]) and (not self.grid[3][7]) and isinstance(self.grid[0][7], Rook) and self.grid[0][7].color == PIECE_LIGHT_COLOR and (not self.grid[0][7].hasMoved):
                                    # move king
                                        self.grid[2][7] = self.grid[4][7]
                                        self.grid[2][7].hasMoved = True
                                        self.grid[4][7] = None
                                        # move rook
                                        self.grid[3][7] = self.grid[0][7]
                                        self.grid[3][7].hasMoved = True
                                        self.grid[0][7] = None
                                finally:
                                    self.gridLocks[1][7].release()
                                    self.gridLocks[3][7].release()
                                    self.gridLocks[0][7].release()

                            # check kingside castle for white is valid
                            if dest == (6, 7) and self.gridLocks[5][7].acquire(timeout=1) and self.gridLocks[7][7].acquire(timeout=1): 
                                try:
                                    if (not self.grid[5][7]) and (not self.grid[6][7]) and isinstance(self.grid[7][7], Rook) and self.grid[7][7].color == PIECE_LIGHT_COLOR and (not self.grid[7][7].hasMoved):
                                        # move king
                                        self.grid[6][7] = self.grid[4][7]
                                        self.grid[6][7].hasMoved = True
                                        self.grid[4][7] = None
                                        # move rook
                                        self.grid[5][7] = self.grid[7][7]
                                        self.grid[5][7].hasMoved = True
                                        self.grid[7][7] = None
                                finally:
                                    self.gridLocks[5][7].release()
                                    self.gridLocks[7][7].release()
                        else:
                            # check queenside castle for black is valid
                            if dest == (2, 0) and self.gridLocks[1][0].acquire(timeout=1) and self.gridLocks[3][0].acquire(timeout=1) and self.gridLocks[0][0].acquire(timeout=1):
                                try:
                                    if (not self.grid[1][0]) and (not self.grid[2][0]) and (not self.grid[3][0]) and isinstance(self.grid[0][0], Rook) and self.grid[0][0].color == PIECE_DARK_COLOR and (not self.grid[0][0].hasMoved):
                                        # move king
                                        self.grid[2][0] = self.grid[4][0]
                                        self.grid[2][0].hasMoved = False
                                        self.grid[4][0] = None
                                        # move rook
                                        self.grid[3][0] = self.grid[0][0]
                                        self.grid[3][0].hasMoved = True
                                        self.grid[0][0] = None
                                finally:
                                    self.gridLocks[1][0].release()
                                    self.gridLocks[3][0].release()
                                    self.gridLocks[0][0].release()

                            # check kingside castle for black is valid
                            if dest == (6, 0) and self.gridLocks[5][0].acquire(timeout=1) and self.gridLocks[7][0].acquire(timeout=1):
                                try:
                                    if (not self.grid[5][0]) and (not self.grid[6][0]) and isinstance(self.grid[7][0], Rook) and self.grid[7][0].color == PIECE_DARK_COLOR and (not self.grid[7][0].hasMoved):
                                        # move king
                                        self.grid[6][0] = self.grid[4][0]
                                        self.grid[6][0].hasMoved = False
                                        self.grid[4][0] = None
                                        # move rook
                                        self.grid[5][0] = self.grid[7][0]
                                        self.grid[5][0].hasMoved = True
                                        self.grid[7][0] = None
                                finally:
                                    self.gridLocks[5][0].release()
                                    self.gridLocks[7][0].release()
                        
                        return True

                # check if there's a piece in the way
                if (self.grid[src_col][src_row].can_move(src, dest)):
                    passed = self.grid[src_col][src_row].pass_through(src, dest)
                    for (i,j) in passed:
                        if self.grid[i][j]:
                            return False # piece in the way
                else:
                    return False
                
                # check if your destination is a piece of the same color
                if self.grid[dest_col][dest_row]:
                    if self.grid[dest_col][dest_row].color == self.grid[src_col][src_row].color:
                        return False # friendly fire
                
                # Successful move
                if self.grid[dest_col][dest_row]:
                    self.captured.append(self.grid[dest_col][dest_row].toString())
                self.grid[dest_col][dest_row] = self.grid[src_col][src_row]
                self.grid[src_col][src_row] = None
                self.grid[dest_col][dest_row].updateTimer(time.perf_counter())
                self.winner = possible_winner
                
                # if the king or rook have moved
                if isinstance(self.grid[dest_col][dest_row], King) or \
                  isinstance(self.grid[dest_col][dest_row], Rook):
                  self.grid[dest_col][dest_row].hasMoved = True
                
                return True
            
            finally:
                self.gridLocks[src_col][src_row].release()
                self.gridLocks[dest_col][dest_row].release()
        else:
            return False
    
    def click(self, click_coordinates, playerColor):
        (click_col, click_row) = click_coordinates
        if self.grid[click_col][click_row] and self.grid[click_col][click_row].color == playerColor:
            return self.grid[click_col][click_row]
        
    def capturedPieces(self):
        return self.captured
        
    def grid_to_string(self):     
        s = ""
        for i in range(self.length):
            for j in range(self.length):
                if self.grid[i][j]:
                    s += (self.grid[i][j].toString() + ",")
                else:
                    s += ".,"
        s = s[:-1]
        if self.winner:
            return self.winner + s
        else:
            return s
