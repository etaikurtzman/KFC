from network import Network
import pygame
import threading

BOARD_LENGTH = 800

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
        # self.stop_event = threading.Event()

    

    def getUpdatesLoop(self):
        while True:
            board = self.network.receive()
            self.screen.fill('yellow')
            self.draw_board()
            self.draw_pieces(board)
            
            pygame.draw.circle(self.screen, (200, 0, 255), (BOARD_LENGTH - 250, BOARD_LENGTH - 250), 75)

            pygame.display.update()
    
    
    def getMovesLoop(self):
        print("In getMovesLoop!")
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    # self.stop_event.set()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_x, mouse_y = event.pos
                        start = (mouse_x // (BOARD_LENGTH // 8), mouse_y // (BOARD_LENGTH // 8))

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        mouse_x, mouse_y = event.pos
                        end = (mouse_x // (BOARD_LENGTH // 8), mouse_y // (BOARD_LENGTH // 8))
                        if start and end:
                            self.network.sendMove(str((start, end)))
                        start = None
                        end = None
            
        pygame.quit()


    def get_image(self, piece_string):
        piece_images = {
            'wb': pygame.image.load('imgs/w_bishop.png'),
            'bb': pygame.image.load('imgs/b_bishop.png'),
            'wk': pygame.image.load('imgs/w_king.png'),
            'bk': pygame.image.load('imgs/b_king.png'),
            'wn': pygame.image.load('imgs/w_knight.png'),
            'bn': pygame.image.load('imgs/b_knight.png'),
            'wp': pygame.image.load('imgs/w_pawn.png'),
            'bp': pygame.image.load('imgs/b_pawn.png'),
            'wq': pygame.image.load('imgs/w_queen.png'),
            'bq': pygame.image.load('imgs/b_queen.png'),
            'wr': pygame.image.load('imgs/w_rook.png'),
            'br': pygame.image.load('imgs/b_rook.png')
        }
        return piece_images.get(piece_string)
 
    def draw_pieces(self, encoded_board):
        decoded_board = encoded_board.split(',')
        index = 0
        for i in range(self.length):
            for j in range(self.length):
                if decoded_board[index] != ".":
                    piece_image = self.get_image(decoded_board[index])
                    piece_image = pygame.transform.scale(piece_image, (100, 100))
                    self.screen.blit(piece_image, ((i * (self.pixelLength // self.length)), (j * (self.pixelLength // self.length))))
                index += 1

    def draw_board(self):
        print("draw_board called")
        self.screen.fill('yellow')
        for i in range(0, 8):
            for j in range(0, 8):
                if ((i + j) % 2 == 1):
                    square_dim = BOARD_LENGTH / 8
                    pygame.draw.rect(self.screen, 'orange', (i * square_dim, j * square_dim, BOARD_LENGTH / 8, BOARD_LENGTH / 8))
            


if __name__ == '__main__':
    main()