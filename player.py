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

LIGHT_SQUARE_COLOR = (145, 184, 194) # RGB value
DARK_SQUARE_COLOR = (65, 104, 130) # RGB value

BUTTON_COLOR = (108, 222, 122) # RGB value
# Coordinates where a button will display on the board
BUTTON_POS = (400, 350)
# Padding within a button (in pixels)
BUTTON_PADDING = 10

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
    serverIP = input("Enter the server's IPv4: ")
    player = Player(serverIP)

    # Begin thread that listens for board updates
    updateThread = threading.Thread(target=player.get_updates_loop)
    updateThread.start()

    # Begin loop that listens for player moves
    player.get_moves_loop()

    updateThread.join()


class Player:
    def __init__(self, serverIP):
        pygame.init()
        
        # Communication with the server
        self.network = Network(serverIP)
        # Player's color - white or black
        self.color = self.network.getColor()
        # Player's pygame screen
        self.screen = pygame.display.set_mode([BOARD_LENGTH, BOARD_LENGTH])
        
        # Indicate whether or not a player has won
        self.winner = False
        # If the start screen is being displayed or not
        self.startScreen = True
        # If the waiting screen is displayed
        self.waiting = False

        # Coordinates of last time player clicks on its own piece
        self.clickedCoordinates = None
        # Coordinates of last piece player successfully moved
        self.draggedCoordinates = None
        # Coordinates of last time the other player successfully moved a piece
        self.otherCoordinates = None
        
        # List of current pieces on cooldown
        self.pieceCooldowns = []
        # Lock to protect pieceCooldowns
        self.cooldownLock = threading.Lock()
        
        # string representation of last encoded board
        self.currentEncodedBoard = None


    def get_updates_loop(self):
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
                
                with self.cooldownLock:
                    self.pieceCooldowns.append(gridCoords)
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
        running = True
        startPos = None
        
        while running:
            # Process pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.network.sendQuit()
                    break
    
                if self.waiting:
                    pygame.mouse.set_cursor(CURSOR1)
                    self.draw_game_state()
                    self.draw_button(*self.create_button(
                                        "Waiting for other player to join...", 
                                        50))
                else:
                    startPos = self.process_event(event, startPos)

        pygame.quit()
    

    def process_event(self, event, startPos):
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
                    self.network.sendStart()
                    self.waiting = True
                    self.startScreen = False

            # Send the click message
            elif startPos:
                self.network.sendClick(str(startPos))
        
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
                self.network.sendMove(str((startPos, end)))
            startPos = None

        return startPos


    def cooldown_timer(self, cooldownTime, pieceCoordinates):
        time.sleep(cooldownTime)

        # Remove piece's cooldown
        with self.cooldownLock:
            if (pieceCoordinates in self.pieceCooldowns) and (not self.winner): 
                self.pieceCooldowns.remove(pieceCoordinates)
                self.draw_game_state()
                pygame.display.update()


    def draw_countdown(self):
        self.draw_board()
        self.draw_pieces()
        
        count = 3
        while count > 0:
            self.draw_button(*self.create_button(str(count) + "...", 100))
            self.draw_board()
            self.draw_pieces()
            time.sleep(1)
            count -= 1
        
        self.draw_button(*self.create_button("Go!", 100))
        time.sleep(1)
    

    def get_coordinates(self, x, y):
        if self.color == "black":
            screenX = (GRID_LENGTH - 1 - x) * SQUARE_LENGTH
            screenY = (GRID_LENGTH - 1 - y) * SQUARE_LENGTH
        if self.color == "white":
            screenX = x * SQUARE_LENGTH
            screenY = y * SQUARE_LENGTH
        return (screenX, screenY)
    

    def get_grid_coordinates(self, x, y):
        if self.color == "black":
            gridX = (GRID_LENGTH - 1 - x)
            gridY = (GRID_LENGTH - 1 - y)
        if self.color == "white":
            gridX = x
            gridY = y
        return (gridX, gridY)


    def create_button(self, text, fontSize):
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
        pygame.draw.rect(self.screen, BUTTON_COLOR, buttonRect)
        pygame.draw.rect(self.screen, "black", buttonRect, 2)
        self.screen.blit(
            buttonText, 
            (buttonRect.left + BUTTON_PADDING, buttonRect.top + BUTTON_PADDING))
        pygame.display.update()
    

    def draw_colored_squares(self):
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
        (newX, newY) = self.get_coordinates(x, y)
        pygame.draw.rect(self.screen, color, 
                                    (newX, newY, SQUARE_LENGTH, SQUARE_LENGTH))


    def draw_pieces(self):
        decodedBoard = self.currentEncodedBoard.split(',')
        if self.color == "black":
            decodedBoard.reverse()
        
        index = 0
        pieceincooldown = False
        for i in range(GRID_LENGTH):
            for j in range(GRID_LENGTH):
                pieceincooldown = (i, j) in self.pieceCooldowns
                if decodedBoard[index] != ".":
                    if pieceincooldown:
                        pieceImage = COOLDOWN_IMAGES.get(decodedBoard[index])
                    else:
                        pieceImage = PIECE_IMAGES.get(decodedBoard[index])
                    self.screen.blit(pieceImage, 
                                        (i * SQUARE_LENGTH, j * SQUARE_LENGTH))
                index += 1


    def draw_board(self):
        self.screen.fill(LIGHT_SQUARE_COLOR)
        for i in range(0, GRID_LENGTH):
            for j in range(0, GRID_LENGTH):
                if ((i + j) % 2 == 1):
                    pygame.draw.rect(self.screen, 
                                     DARK_SQUARE_COLOR, 
                                     (i * SQUARE_LENGTH, 
                                      j * SQUARE_LENGTH, 
                                      SQUARE_LENGTH, 
                                      SQUARE_LENGTH))


    def draw_game_state(self):
        self.draw_board()
        self.draw_colored_squares()
        self.draw_pieces()


if __name__ == '__main__':
    main()