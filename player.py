from network import Network
import pygame
import threading
import time

BOARD_LENGTH = 800


piece_images = {
            'wb': pygame.transform.scale(pygame.image.load('imgs/wB.png'), (100, 100)),
            'bb': pygame.transform.scale(pygame.image.load('imgs/bB.png'), (100, 100)),
            'wk': pygame.transform.scale(pygame.image.load('imgs/wK.png'), (100, 100)),
            'bk': pygame.transform.scale(pygame.image.load('imgs/bK.png'), (100, 100)),
            'wn': pygame.transform.scale(pygame.image.load('imgs/wN.png'), (100, 100)),
            'bn': pygame.transform.scale(pygame.image.load('imgs/bN.png'), (100, 100)),
            'wp': pygame.transform.scale(pygame.image.load('imgs/wP.png'), (100, 100)),
            'bp': pygame.transform.scale(pygame.image.load('imgs/bP.png'), (100, 100)),
            'wq': pygame.transform.scale(pygame.image.load('imgs/wQ.png'), (100, 100)),
            'bq': pygame.transform.scale(pygame.image.load('imgs/bQ.png'), (100, 100)),
            'wr': pygame.transform.scale(pygame.image.load('imgs/wR.png'), (100, 100)),
            'br': pygame.transform.scale(pygame.image.load('imgs/bR.png'), (100, 100))
        }

cool_piece_images = {
            'wb': pygame.transform.scale(pygame.image.load('imgs/rB.png'), (100, 100)),
            'bb': pygame.transform.scale(pygame.image.load('imgs/rB.png'), (100, 100)),
            'wk': pygame.transform.scale(pygame.image.load('imgs/rK.png'), (100, 100)),
            'bk': pygame.transform.scale(pygame.image.load('imgs/rK.png'), (100, 100)),
            'wn': pygame.transform.scale(pygame.image.load('imgs/rN.png'), (100, 100)),
            'bn': pygame.transform.scale(pygame.image.load('imgs/rN.png'), (100, 100)),
            'wp': pygame.transform.scale(pygame.image.load('imgs/rP.png'), (100, 100)),
            'bp': pygame.transform.scale(pygame.image.load('imgs/rP.png'), (100, 100)),
            'wq': pygame.transform.scale(pygame.image.load('imgs/rQ.png'), (100, 100)),
            'bq': pygame.transform.scale(pygame.image.load('imgs/rQ.png'), (100, 100)),
            'wr': pygame.transform.scale(pygame.image.load('imgs/rR.png'), (100, 100)),
            'br': pygame.transform.scale(pygame.image.load('imgs/rR.png'), (100, 100))
        }

def main():
    serverIP = input("Enter the server's IPv4: ")
    player = Player(serverIP)
    update_thread = threading.Thread(target=player.getUpdatesLoop)
    update_thread.start()
    player.getMovesLoop()
    update_thread.join()


class Player:
    def __init__(self, serverIP):
        self.network = Network(serverIP)
        self.color = self.network.getColor()
        pygame.init()
        self.screen = pygame.display.set_mode([BOARD_LENGTH, BOARD_LENGTH])
        self.length = 8
        self.pixelLength = BOARD_LENGTH
        self.winner = False
        self.draggedPiece = None
        
        self.clickedPiece = False
        self.clickedCoordinates = None
        
        self.draggingPiece = False
        self.draggedCoordinates = None
        
        self.otherPiece = False
        self.otherCoordinates = None
        
        self.pieceCooldowns = []
        self.cooldown_lock = threading.Lock()
        self.current_encoded_board = None

    def getUpdatesLoop(self):
        running = True
        while running:
            # if self.winner:
            #     break
            mailbox = self.network.receive()
            msgs = mailbox.split('|')
            for msg in msgs:
                # print("msg is: ", msg)
                if msg != '':
                    print("in player msg is:", msg)
                    if msg[0:5] == "white":
                        self.screen.fill('yellow')
                        self.draw_board()
                        self.current_encoded_board = msg[5:]
                        self.draw_pieces()
                        font = pygame.font.Font(None, 100) #100 font size
                        text = font.render('White Wins!', True, (255, 0, 53)) #redish
                        self.screen.blit(text, (200, 325))
                        pygame.display.update()
                        self.winner = True
                        running = False
                    elif msg[0:5] == "black":
                        self.screen.fill('yellow')
                        self.draw_board()
                        self.current_encoded_board = msg[5:]
                        self.draw_pieces()
                        font = pygame.font.Font(None, 100) #100 font size
                        text = font.render('Black Wins!', True, (255, 0, 53)) #redish
                        self.screen.blit(text, (200, 325))
                        pygame.display.update()
                        self.winner = True
                        running = False
                    elif msg == "Quit":
                        running = False
                    elif msg.startswith("CLICKED:"):
                        (clicked_coordinates, clicked_piece) = eval(msg[len("CLICKED:"):])
                        self.draggingPiece = piece_images.get(clicked_piece)
                        print("piece just returned is: ", self.draggingPiece)
                        
                        self.clickedPiece = True
                        self.clickedCoordinates = clicked_coordinates
                    elif msg.startswith("END:"):
                        print("in END message receive")
                        msgs = msg[len("END:"):].split(';')
                        print("in END: msgs is: ", msgs)
                        
                        dragged_coordinates = eval(msgs[0])
                        print("dragged_coordinates: ", dragged_coordinates)
                        cooldown = float(msgs[1])
                        print("cooldown: ", cooldown)
                        
                        print("before lock in getUpdates")
                        with self.cooldown_lock:
                            print("in lock in getUpdates")
                            self.pieceCooldowns.append(self.get_grid_coordinates(dragged_coordinates[0], dragged_coordinates[1]))
                            
                        cooldown_thread = threading.Thread(target=self.cooldown_timer, args=[cooldown, self.get_grid_coordinates(dragged_coordinates[0], dragged_coordinates[1])])
                        cooldown_thread.start()
                        
                        self.draggedPiece = True
                        self.draggedCoordinates = dragged_coordinates
                    elif msg.startswith("END-OTHER:"):
                        other_coordinates = eval(msg[len("END-OTHER:"):])
                        print("other_coordinates: ", other_coordinates)
                        self.otherPiece = True
                        self.otherCoordinates = other_coordinates
                        if other_coordinates in self.pieceCooldowns:
                            print("if other is in cooldown list")
                            self.pieceCooldowns.remove(other_coordinates)
                    else:
                        board = msg
                        self.current_encoded_board = board
                    
                    if running:
                        with self.cooldown_lock:
                            self.draw_board()
                            
                            if self.clickedPiece == True:
                                self.draw_clicked()
                            if self.draggedPiece == True:
                                self.draw_dragged()
                            if self.otherPiece == True:
                                self.draw_other() 
                            self.draw_pieces()
                            
                            pygame.display.update()

    def getMovesLoop(self):
        running = True
        
        cursor1 = pygame.SYSTEM_CURSOR_ARROW
        cursor2 = pygame.SYSTEM_CURSOR_HAND
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.network.sendQuit()
                    break
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pygame.mouse.set_cursor(cursor2)
                        mouse_x, mouse_y = event.pos
                        # rotate 180 degrees for player with black pieces
                        if self.color == "black":
                            mouse_x = BOARD_LENGTH - 1 - mouse_x
                            mouse_y = BOARD_LENGTH - 1 - mouse_y
                        start = (mouse_x // (BOARD_LENGTH // 8), mouse_y // (BOARD_LENGTH // 8))
                        if start:
                            self.network.sendClick(str(start))
                
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        pygame.mouse.set_cursor(cursor1)
                        mouse_x, mouse_y = event.pos
                        # rotate 180 degrees for player with black pieces
                        if self.color == "black":
                            mouse_x = BOARD_LENGTH - 1 - mouse_x
                            mouse_y = BOARD_LENGTH - 1 - mouse_y
                        end = (mouse_x // (BOARD_LENGTH // 8), mouse_y // (BOARD_LENGTH // 8))
                        if start and end:
                            self.network.sendMove(str((start, end)))
                        start = None
                        end = None
        pygame.quit()
        print("quitting getmovesloop")
    
    def cooldown_timer(self, cooldown_time, piece_coordinates):
        print("cooldown timer thread started")
        print("self.pieceCooldown[] before sleep:", self.pieceCooldowns)
        time.sleep(cooldown_time)
        print()
        
        with self.cooldown_lock:
            print("in lock")
            if piece_coordinates in self.pieceCooldowns and (not self.winner): 
                print("in thread, making sure piece is still in the cooldown list")
                self.pieceCooldowns.remove(piece_coordinates)
                self.draw_board()

                self.draw_dragged()
                self.draw_clicked()
                self.draw_other()
                print("before thread calls draw_pieces")
                self.draw_pieces()
                print("after thread calls draw pieces")
                pygame.display.update()
                print("self.pieceCooldown[] after sleep:", self.pieceCooldowns)

        
    def draw_clicked(self):
        if self.clickedCoordinates:
            self.draw_clicked_and_dragged_squares(self.clickedCoordinates[0], self.clickedCoordinates[1], 'cyan')
        
    def draw_dragged(self):
        if self.draggedCoordinates:
            self.draw_clicked_and_dragged_squares(self.draggedCoordinates[0], self.draggedCoordinates[1], 'blue')
        
    def draw_other(self):
        if self.otherCoordinates:
            self.draw_clicked_and_dragged_squares(self.otherCoordinates[0], self.otherCoordinates[1], 'turquoise') 
    
    def get_coordinates(self, x, y):
        if self.color == "black":
            screen_x = (7 - x) * (BOARD_LENGTH / 8)
            screen_y = (7 - y) * (BOARD_LENGTH / 8)
        if self.color == "white":
            screen_x = x * (BOARD_LENGTH / 8)
            screen_y = y * (BOARD_LENGTH / 8)
        return (screen_x, screen_y)
    
    def get_grid_coordinates(self, x, y):
        if self.color == "black":
            grid_x = (7 - x)
            grid_y = (7 - y)
        if self.color == "white":
            grid_x = x
            grid_y = y
        return (grid_x, grid_y)

    def draw_pieces(self):
        print("in draw_pieces")
        decoded_board = self.current_encoded_board.split(',')
        if self.color == "black":
            decoded_board.reverse()
        
        index = 0
        pieceincooldown = False
        for i in range(self.length):
            for j in range(self.length):
                pieceincooldown = (i, j) in self.pieceCooldowns
                #print("self.pieceCooldowns is: ", self.pieceCooldowns)
                #print("(i, j) is: ", (i, j))
                if decoded_board[index] != ".":
                    if pieceincooldown:
                        #print("in draw_pieces, if cooldown piece")
                        piece_image = cool_piece_images.get(decoded_board[index])
                        #print("piece_image is:", piece_image)
                    else:
                        piece_image = piece_images.get(decoded_board[index])
                    self.screen.blit(piece_image, ((i * (self.pixelLength // self.length)), (j * (self.pixelLength // self.length))))
                index += 1

    def draw_board(self):
        self.screen.fill((145, 184, 194))
        for i in range(0, 8):
            for j in range(0, 8):
                if ((i + j) % 2 == 1):
                    square_dim = BOARD_LENGTH / 8
                    pygame.draw.rect(self.screen, (65,104,130), (i * square_dim, j * square_dim, BOARD_LENGTH / 8, BOARD_LENGTH / 8))
    
    def draw_clicked_and_dragged_squares(self, x, y, color):
        (new_x, new_y) = self.get_coordinates(x, y)
        pygame.draw.rect(self.screen, color, (new_x, new_y, BOARD_LENGTH / 8, BOARD_LENGTH / 8))

if __name__ == '__main__':
    main()