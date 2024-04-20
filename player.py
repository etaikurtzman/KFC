# player.py
# 
# 

from network import Network
import pygame
import threading

BOARD_LENGTH = 800

piece_images = {
            'wb': pygame.transform.scale(pygame.image.load('imgs/w_bishop.png'), (100, 100)),
            'bb': pygame.transform.scale(pygame.image.load('imgs/b_bishop.png'), (100, 100)),
            'wk': pygame.transform.scale(pygame.image.load('imgs/w_king.png'), (100, 100)),
            'bk': pygame.transform.scale(pygame.image.load('imgs/b_king.png'), (100, 100)),
            'wn': pygame.transform.scale(pygame.image.load('imgs/w_knight.png'), (100, 100)),
            'bn': pygame.transform.scale(pygame.image.load('imgs/b_knight.png'), (100, 100)),
            'wp': pygame.transform.scale(pygame.image.load('imgs/w_pawn.png'), (100, 100)),
            'bp': pygame.transform.scale(pygame.image.load('imgs/b_pawn.png'), (100, 100)),
            'wq': pygame.transform.scale(pygame.image.load('imgs/w_queen.png'), (100, 100)),
            'bq': pygame.transform.scale(pygame.image.load('imgs/b_queen.png'), (100, 100)),
            'wr': pygame.transform.scale(pygame.image.load('imgs/w_rook.png'), (100, 100)),
            'br': pygame.transform.scale(pygame.image.load('imgs/b_rook.png'), (100, 100))
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

    def getUpdatesLoop(self):
        while True:
            msg = self.network.receive()
            #print(msg)
            if msg[0:5] == "white":
                self.screen.fill('yellow')
                self.draw_board()
                self.draw_pieces(msg[5:])
                font = pygame.font.Font(None, 100) #100 font size
                text = font.render('White Wins!', True, (50, 50, 255)) #bluish
                self.screen.blit(text, (200, 325))
                pygame.display.update()
                break
            elif msg[0:5] == "black":
                self.screen.fill('yellow')
                self.draw_board()
                self.draw_pieces(msg[5:])
                font = pygame.font.Font(None, 100) #100 font size
                text = font.render('Black Wins!', True, (50, 50, 255)) #bluish
                self.screen.blit(text, (200, 325))
                pygame.display.update()
                break
            elif msg == "Quit":
                break
            board = msg
            self.screen.fill('yellow')
            self.draw_board()
            self.draw_pieces(board)
            
            pygame.draw.circle(self.screen, (200, 0, 255), (BOARD_LENGTH - 250, BOARD_LENGTH - 250), 75)
            
            pygame.display.update()

    def getMovesLoop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.network.sendMove("Quit")
                    # self.stop_event.set()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_x, mouse_y = event.pos
                        # rotate 180 degrees for player with black pieces
                        if self.color == "black":
                            mouse_x = BOARD_LENGTH - 1 - mouse_x
                            mouse_y = BOARD_LENGTH - 1 - mouse_y
                        start = (mouse_x // (BOARD_LENGTH // 8), mouse_y // (BOARD_LENGTH // 8))
                        #print(start)
                
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        mouse_x, mouse_y = event.pos
                        # rotate 180 degrees for player with black pieces
                        if self.color == "black":
                            mouse_x = BOARD_LENGTH - 1 - mouse_x
                            mouse_y = BOARD_LENGTH - 1 - mouse_y
                        end = (mouse_x // (BOARD_LENGTH // 8), mouse_y // (BOARD_LENGTH // 8))
                        #print(end)
                        if start and end:
                            self.network.sendMove(str((start, end)))
                        #print("move sent")
                        start = None
                        end = None
        pygame.quit()
        



    def draw_pieces(self, encoded_board):
        decoded_board = encoded_board.split(',')
        if self.color == "black":
            decoded_board.reverse()
        index = 0
        for i in range(self.length):
            for j in range(self.length):
                if decoded_board[index] != ".":
                    piece_image = piece_images.get(decoded_board[index])
                    self.screen.blit(piece_image, ((i * (self.pixelLength // self.length)), (j * (self.pixelLength // self.length))))
                index += 1

    def draw_board(self):
        self.screen.fill('yellow')
        for i in range(0, 8):
            for j in range(0, 8):
                if ((i + j) % 2 == 1):
                    square_dim = BOARD_LENGTH / 8
                    pygame.draw.rect(self.screen, 'orange', (i * square_dim, j * square_dim, BOARD_LENGTH / 8, BOARD_LENGTH / 8))

if __name__ == '__main__':
    main()