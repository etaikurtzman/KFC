'''
player.py
Contains implementation for player class
Handles player input and output using pygame's display GUI
4/29
'''

from network import Network
import pygame
import threading
import time

# Length of the board (in pixels)
BOARD_LENGTH = 800
# Length of the grid (number of squares)
GRID_LENGTH = 8
# Length of each square (in pixels)
SQUARE_LENGTH = BOARD_LENGTH // GRID_LENGTH
# Size of each piece image (in pixels)
IMAGE_SIZE = (SQUARE_LENGTH, SQUARE_LENGTH)

# RGB values to fill the squares on the board
LIGHT_SQUARE_COLOR = (145, 184, 194)
DARK_SQUARE_COLOR = (65, 104, 130)

# button color
BUTTON_COLOR = (108, 222, 122)
# Coordinates where a button will display on the board
BUTTON_POS = (400, 350)
# Padding within a button (in pixels)
BUTTON_PADDING = 10

# dursor displays
CURSOR1 = pygame.SYSTEM_CURSOR_ARROW
CURSOR2 = pygame.SYSTEM_CURSOR_HAND

# Loaded in piece images
PIECE_IMAGES = {
    'wb': pygame.transform.scale(pygame.image.load('imgs/wB.png'), IMAGE_SIZE),
    'bb': pygame.transform.scale(pygame.image.load('imgs/bB.png'), IMAGE_SIZE),
    'wk': pygame.transform.scale(pygame.image.load('imgs/wK.png'), IMAGE_SIZE),
    'bk': pygame.transform.scale(pygame.image.load('imgs/bK.png'), IMAGE_SIZE),
    'wn': pygame.transform.scale(pygame.image.load('imgs/wN.png'), IMAGE_SIZE),
    'bn': pygame.transform.scale(pygame.image.load('imgs/bN.png'), IMAGE_SIZE),
    'wp': pygame.transform.scale(pygame.image.load('imgs/wP.png'), IMAGE_SIZE),
    'bp': pygame.transform.scale(pygame.image.load('imgs/bP.png'), IMAGE_SIZE),
    'wq': pygame.transform.scale(pygame.image.load('imgs/wQ.png'), IMAGE_SIZE),
    'bq': pygame.transform.scale(pygame.image.load('imgs/bQ.png'), IMAGE_SIZE),
    'wr': pygame.transform.scale(pygame.image.load('imgs/wR.png'), IMAGE_SIZE),
    'br': pygame.transform.scale(pygame.image.load('imgs/bR.png'), IMAGE_SIZE)
}

# Loaded in images for pieces on cooldown
COOLDOWN_IMAGES = {
    'wb': pygame.transform.scale(pygame.image.load('imgs/rB.png'), IMAGE_SIZE),
    'bb': pygame.transform.scale(pygame.image.load('imgs/rB.png'), IMAGE_SIZE),
    'wk': pygame.transform.scale(pygame.image.load('imgs/rK.png'), IMAGE_SIZE),
    'bk': pygame.transform.scale(pygame.image.load('imgs/rK.png'), IMAGE_SIZE),
    'wn': pygame.transform.scale(pygame.image.load('imgs/rN.png'), IMAGE_SIZE),
    'bn': pygame.transform.scale(pygame.image.load('imgs/rN.png'), IMAGE_SIZE),
    'wp': pygame.transform.scale(pygame.image.load('imgs/rP.png'), IMAGE_SIZE),
    'bp': pygame.transform.scale(pygame.image.load('imgs/rP.png'), IMAGE_SIZE),
    'wq': pygame.transform.scale(pygame.image.load('imgs/rQ.png'), IMAGE_SIZE),
    'bq': pygame.transform.scale(pygame.image.load('imgs/rQ.png'), IMAGE_SIZE),
    'wr': pygame.transform.scale(pygame.image.load('imgs/rR.png'), IMAGE_SIZE),
    'br': pygame.transform.scale(pygame.image.load('imgs/rR.png'), IMAGE_SIZE)
}

def main():
    # connect to server abd get player address
    serverIP = input("Enter the server's IPv4: ")
    player = Player(serverIP)

    # Begin thread that listens for board updates
    updateThread = threading.Thread(target=player.get_updates_loop)
    updateThread.start()

    # Begin loop that listens for player moves
    player.get_moves_loop()
    updateThread.join()


class Player:
    """
    A class to represent the player and its logic.

    Members
    -------
    Network: self.network 
        The network that handles communication between the player and the server
        
    Player Color: self.color 
        Player's color - white or black
        
    Winner: self.winner
        Indicate whether or not a player has won and controls when the game 
        starts and ends.

    Start Screen: self.startScreen
        Boolean indicating if the start screen is being displayed or not.

    Waiting Screen: self.waiting
        Boolean indicating if the waiting screen is displayed or not.

    Clicked Coordinates: self.clickedCoordinates
        Coordinates of the last time player clicks on its own piece.

    Dragged Coordinates: self.draggedCoordinates
        Coordinates of the last piece player successfully moved.

    Other Player's coordinates: self.otherCoordinates
        Coordinates of last time the other player successfully moved a piece.

    Cooldown Array: self.pieceCooldowns
        List of current pieces in cooldown.

    Cooldown lock: self.cooldownLock
        A threading lock to protect pieceCooldowns.

    Board: self.currentEncodedBoard
        String representation of the last encoded board state.


    Functions
    ---------
    self.get_updates_loop():
        Continuously listens for updates from the server and processes them. 
        Also draws the current game state after each update is recieved and 
        processed. 

    self.process_updates(msg):
        Processes a single update message received from the server.

    self.get_moves_loop():
        Continuously listens for player moves from player clicking the screen 
        and processes them.

    self.process_event(event, startPos):
        Processes pygame events and updates the game state accordingly.

    self.cooldown_timer(cooldownTime, pieceCoordinates):
        Initiates a cooldown timer for a piece and removes it from cooldown when
        expired.

    self.draw_countdown():
        Draws the countdown on the screen before the game starts.

    self.get_coordinates(x, y):
        Converts grid coordinates to screen coordinates specific to white or 
        black.

    self.get_grid_coordinates(x, y):
        Converts screen coordinates to grid coordinates specific to white or 
        black.

    self.create_button(text, fontSize):
        Creates a button with the specified text and font size and returns it.

    self.draw_button(buttonText, buttonRect):
        Draws a button on the screen.

    self.draw_colored_squares():
        Draws colored squares on the board (clicked, dragged and other).

    self.draw_clicked_and_dragged_squares(x, y, color):
        Draws a square on the board with the specified color for either clicked, 
        dragged or other.

    self.draw_pieces():
        Draws the pieces on the board.

    self.draw_board():
        Draws the chessboard on the screen.

    self.draw_game_state():
        Draws the current game state (pieces, colored squares and board) on 
        the screen. 
    """
    def __init__(self, serverIP):
        pygame.init()
        
        self.network = Network(serverIP)
        self.color = self.network.get_color()
        self.screen = pygame.display.set_mode([BOARD_LENGTH, BOARD_LENGTH])
        
        self.winner = False
        self.startScreen = True
        self.waiting = False

        self.clickedCoordinates = None
        self.draggedCoordinates = None
        self.otherCoordinates = None
        
        self.pieceCooldowns = []
        self.cooldownLock = threading.Lock()
        
        self.currentEncodedBoard = None

    def get_updates_loop(self):
        """
        Continuously listens for updates from the server and processes them.
        Also draws the current game state after each update is received and 
        processed.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        # Begin updates loop
        while not self.winner:
            # Wait until a message is received from the server
            mailbox = self.network.receive()
            if not mailbox:
                continue

            # Process messages
            msgs = mailbox.split('|')
            for msg in msgs:
                if msg:
                    self.process_update(msg)

                    # Draw the board if there's not a winner
                    if not self.winner:
                        with self.cooldownLock:
                            self.draw_game_state()

                            if self.startScreen:
                                self.draw_button(*self.create_button("Start", 
                                                                      100))
                            pygame.display.update()
    
    
    def process_update(self, msg):
        """
        Processes a single update message received from the server.

        Parameters
        ----------
        msg : str
            The message received from the server.

        Returns
        -------
        None
        
        """
        msgParts = msg.split(':')
        match msgParts[0]:
            # Start the game
            case "READY":
                self.waiting = False
                self.draw_countdown()

            # Display the clicked color
            case "CLICKED":
                self.clickedCoordinates = eval(msgParts[1])

            # Update cooldowns corresponding to this player's move
            case "END":       
                self.draggedCoordinates = eval(msgParts[1])
                cooldown = float(msgParts[2])
                gridCoords = self.get_grid_coordinates(
                                self.draggedCoordinates[0],
                                self.draggedCoordinates[1])
                # add the piece to list of pieces in cooldown
                with self.cooldownLock:
                    self.pieceCooldowns.append(gridCoords)

                # start a cooldown thread
                cooldownThread = threading.Thread(
                                    target=self.cooldown_timer, 
                                    args=[cooldown, gridCoords])
                cooldownThread.start()

            # Update cooldowns corresponding to other player's move
            case "END-OTHER":
                self.otherCoordinates = eval(msgParts[1])
                if self.otherCoordinates in self.pieceCooldowns:
                    self.pieceCooldowns.remove(self.otherCoordinates)
            
            # Draw the win screen
            case "white" | "black":
                self.currentEncodedBoard = msgParts[1]
                self.draw_game_state()
                self.draw_button(*self.create_button(
                                    f"{msgParts[0].capitalize()} Wins!", 100))
                self.winner = True
            
            # Quit out of the game
            case "Quit":
                self.winner = True
            
            # Update the board state
            case _:
                self.currentEncodedBoard = msg


    def get_moves_loop(self):
        """
        Continuously listens for player moves from player clicking the screen
        and processes them.

        Parameters
        ----------
        None

        Returns
        -------
        None
        
        """
        running = True
        startPos = None
        
        while running:
            # Process pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.network.send_quit()
                    break
                # waiting screen is being displayed
                if self.waiting:
                    pygame.mouse.set_cursor(CURSOR1)
                    self.draw_game_state()
                    self.draw_button(*self.create_button(
                                        "Waiting for other player to join...", 
                                        50))
                # process events
                else:
                    startPos = self.process_event(event, startPos)

        pygame.quit()
    

    def process_event(self, event, startPos):
        """
        Processes pygame events and updates the game state accordingly.

        Parameters
        ----------
        event : pygame.Event
            The pygame event to be processed.
        startPos : tuple or None
            The starting position of the piece being moved.

        Returns
        -------
        startPos : tuple or None
            The updated starting position of the piece being moved.
        
        """
        # On button press
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pygame.mouse.set_cursor(CURSOR2)
            mouseX, mouseY = event.pos

            # rotate 180 degrees for player with black pieces
            if self.color == "black":
                mouseX = BOARD_LENGTH - 1 - mouseX
                mouseY = BOARD_LENGTH - 1 - mouseY

            startPos = (mouseX // SQUARE_LENGTH, mouseY // SQUARE_LENGTH)

            # Start the game
            if self.startScreen:
                startText, startButton = self.create_button("Start", 100)
                self.draw_button(startText, startButton)

                if startButton.collidepoint(event.pos):
                    self.network.send_start()
                    self.waiting = True
                    self.startScreen = False

            # Send the click message
            elif startPos:
                self.network.send_click(str(startPos))
        
        # On button release
        if event.type == pygame.MOUSEBUTTONUP and (not self.startScreen) \
                                              and event.button == 1:
            pygame.mouse.set_cursor(CURSOR1)
            mouseX, mouseY = event.pos

            # rotate 180 degrees for player with black pieces
            if self.color == "black":
                mouseX = BOARD_LENGTH - 1 - mouseX
                mouseY = BOARD_LENGTH - 1 - mouseY
            
            end = (mouseX // SQUARE_LENGTH, mouseY // SQUARE_LENGTH)

            # Send the move message
            if startPos and end:
                self.network.send_move(str((startPos, end)))
            startPos = None

        return startPos


    def cooldown_timer(self, cooldownTime, pieceCoordinates):
        """
        Initiates a cooldown timer for a piece and removes it from cooldown 
        when expired.


        Parameters
        ----------
        cooldownTime : float
            The duration of the cooldown timer.
        pieceCoordinates : tuple
            The coordinates of the piece to be put on cooldown.


        Returns
        -------
        None
        
        """
        time.sleep(cooldownTime)

        # Remove the piece from cooldown if the piece hasn't been captured and a player
        # hasn't won.
        with self.cooldownLock:
            if (pieceCoordinates in self.pieceCooldowns) and (not self.winner): 
                self.pieceCooldowns.remove(pieceCoordinates)
                self.draw_game_state()
                pygame.display.update()


    def draw_countdown(self):
        """
        Draws the countdown on the screen before the game starts.

        Parameters
        ----------
        None

        Returns
        -------
        None
        
        """
        self.draw_board()
        self.draw_pieces()
        
        # draw the countdown by creating 3 buttons.
        count = 3
        while count > 0:
            self.draw_button(*self.create_button(str(count) + "...", 100))
            self.draw_board()
            self.draw_pieces()
            time.sleep(1)
            count -= 1
            
        # draw the Go! button
        self.draw_button(*self.create_button("Go!", 100))
        time.sleep(1)
    

    def get_coordinates(self, x, y):
        """
        Converts grid coordinates to screen coordinates specific to white or 
        black.


        Parameters
        ----------
        x : int
            The x-coordinate in the grid.
        y : int
            The y-coordinate in the grid.

        Returns
        -------
        (screenX, screenY) : int
            Tuple containing screen coordinates corresponding to the grid 
            coordinates.
        
        """
        # convert coordinates to pixel locations for each player 
        if self.color == "black":
            screenX = (GRID_LENGTH - 1 - x) * SQUARE_LENGTH
            screenY = (GRID_LENGTH - 1 - y) * SQUARE_LENGTH
        if self.color == "white":
            screenX = x * SQUARE_LENGTH
            screenY = y * SQUARE_LENGTH
        return (screenX, screenY)
    

    def get_grid_coordinates(self, x, y):
        """
        Converts screen coordinates to grid coordinates specific to white or 
        black.

        Parameters
        ----------
        x : int
            The x-coordinate in the grid.
        y : int
            The y-coordinate in the grid.

        Returns
        -------
        (gridX, gridY) : int
            Tuple containing the grid coordinates corresponding to the screen 
            coordinates.
        
        """
        # convert to grid coordinates specific to each player
        if self.color == "black":
            gridX = (GRID_LENGTH - 1 - x)
            gridY = (GRID_LENGTH - 1 - y)
        if self.color == "white":
            gridX = x
            gridY = y
        return (gridX, gridY)


    def create_button(self, text, fontSize):
        """
        Creates a button with the specified text and font size and returns it.

        Parameters
        ----------
        text : str
            The text to be displayed on the button.
        fontSize : int
            The font size of the button text.

        Returns
        -------
        buttonText, buttonRect : pygame.Surface, pygame.Rect
            The rendered button text and its rectangular area
        
        """
        # create font, text and button rectangle
        font = pygame.font.Font(None, fontSize)
        buttonText = font.render(text, True, "black")
        textRect = buttonText.get_rect(center=BUTTON_POS)
        buttonRect = pygame.Rect(
                            textRect.left - BUTTON_PADDING, 
                            textRect.top - BUTTON_PADDING, 
                            textRect.width + (BUTTON_PADDING * 2), 
                            textRect.height + (BUTTON_PADDING * 2))
        
        return buttonText, buttonRect


    def draw_button(self, buttonText, buttonRect):
        """
        Draws a button on the screen.

        Parameters
        ----------
        buttonText : pygame.Surface
            The rendered button text.
        buttonRect : pygame.Rect
            The rectangular area of the button.

        Returns
        -------
        None
        
        """
        # display rectangles and button
        pygame.draw.rect(self.screen, BUTTON_COLOR, buttonRect)
        pygame.draw.rect(self.screen, "black", buttonRect, 2)
        self.screen.blit(
            buttonText, 
            (buttonRect.left + BUTTON_PADDING, buttonRect.top + BUTTON_PADDING))
        pygame.display.update()
    

    def draw_colored_squares(self):
        """
        Draws colored squares on the board (clicked, dragged, and other).

        Parameters
        ----------
        None

        Returns
        -------
        None
        
        """
        # change color of square to cyan after player clicks on its own piece
        if self.clickedCoordinates:
            self.draw_clicked_and_dragged_squares(
                                        self.clickedCoordinates[0], 
                                        self.clickedCoordinates[1], 
                                        'cyan')
        # change color of square to blue for a piece that has just been moved
        if self.draggedCoordinates:
            self.draw_clicked_and_dragged_squares(
                                        self.draggedCoordinates[0], 
                                        self.draggedCoordinates[1], 
                                        'blue')
        # change color of square to turquoise for a move the other player made
        if self.otherCoordinates:
            self.draw_clicked_and_dragged_squares(
                                        self.otherCoordinates[0], 
                                        self.otherCoordinates[1], 
                                        'turquoise') 
        

    def draw_clicked_and_dragged_squares(self, x, y, color):
        """
        Draws a square on the board with the specified color for either clicked,
        dragged, or other.

        Parameters
        ----------
        x : int
            The x-coordinate of the square.
        y : int
            The y-coordinate of the square.
        color : str
            The color of the square.

        Returns
        -------
        None
        
        """
        # get pixel coordinates and draw the square in the specified color.
        (newX, newY) = self.get_coordinates(x, y)
        pygame.draw.rect(self.screen, color, 
                                    (newX, newY, SQUARE_LENGTH, SQUARE_LENGTH))


    def draw_pieces(self):
        """
        Draws the pieces on the board.


        Parameters
        ----------
        None

        Returns
        -------
        None
        
        """
        decodedBoard = self.currentEncodedBoard.split(',')
        # reverse the board if black
        if self.color == "black":
            decodedBoard.reverse()
        
        index = 0
        pieceincooldown = False
        for i in range(GRID_LENGTH):
            for j in range(GRID_LENGTH):
                pieceincooldown = (i, j) in self.pieceCooldowns
                # decode the board
                if decodedBoard[index] != ".":
                    # if the piece is in cooldown display the cooldown image 
                    if pieceincooldown:
                        pieceImage = COOLDOWN_IMAGES.get(decodedBoard[index])
                    else:
                        # get image from piece_image dictionary
                        pieceImage = PIECE_IMAGES.get(decodedBoard[index])
                    # draw piece on screen
                    self.screen.blit(pieceImage, 
                                        (i * SQUARE_LENGTH, j * SQUARE_LENGTH))
                index += 1


    def draw_board(self):
        """
        Draws the chessboard on the screen.

        Parameters
        ----------
        None

        Returns
        -------
        None
        
        """
        # fill screen with light color
        self.screen.fill(LIGHT_SQUARE_COLOR)
        for i in range(0, GRID_LENGTH):
            for j in range(0, GRID_LENGTH):
                if ((i + j) % 2 == 1):
                    # draw dark rectangles over the screen
                    pygame.draw.rect(self.screen, 
                                     DARK_SQUARE_COLOR, 
                                     (i * SQUARE_LENGTH, 
                                      j * SQUARE_LENGTH, 
                                      SQUARE_LENGTH, 
                                      SQUARE_LENGTH))

    def draw_game_state(self):
        """
        Draws the current game state (pieces, colored squares, and board) on 
        the screen.

        Parameters
        ----------
        None

        Returns
        -------
        None
        
        """
        # draw everything
        self.draw_board()
        self.draw_colored_squares()
        self.draw_pieces()


if __name__ == '__main__':
    main()