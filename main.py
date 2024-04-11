# Simple pygame program

# Import and initialize the pygame library
import pygame
import time
from classes.board import Board


def main():
    pygame.init()
    LENGTH = 800
    # Set up the drawing window
    screen = pygame.display.set_mode([LENGTH, LENGTH])

    # Run until the user asks to quit
    running = True
    dragging = False
    piece = None
    board = Board(screen)
    while running:
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    start = (mouse_x // (LENGTH // 8), mouse_y // (LENGTH // 8))

                    
                    # for row in board.grid:
                    #    for p in row:
                    #        if p and p.image.get_rect().collidepoint(event.pos):
                    #            print("piece selected")
                                # dragging = True
                                # piece = p

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    end = (mouse_x // (LENGTH // 8), mouse_y // (LENGTH // 8))
                    if start and end:
                        board.move(start, end)
                    start = None 
                    end = None
                    # dragging = False
                    # piece = None
            # if event.type == pygame.MOUSEMOTION:
            #     print("moving mouse")
            #     if dragging and piece:
            #         print("Dragging")
            #         board.grid[piece].get_rect().move_ip(event.rel)


        pygame.display.flip()
            

        # Fill the background with white
        screen.fill('yellow')
        # pygame.display.update()
        # screen.fill('black')
        # pygame.display.update()
        for i in range(0, 8):
            for j in range(0, 8):
                if ((i + j) % 2 == 1):
                    square_dim = LENGTH / 8
                    pygame.draw.rect(screen, 'orange', (i * square_dim, j * square_dim, LENGTH / 8, LENGTH / 8))

        # Draw a solid blue circle in the center
        pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)
        # rook = pygame.image.load('imgs/b_rook.png')

        # screen.blit(pygame.transform.scale(rook, (100, 100)), (0, 0))
        board.draw()
        pygame.display.update()
        # pygame.time.wait(1000)
        # board.move((0, 0), (0, 7))
        # board.move((1, 0), (2, 2))
        # board.move((2, 0), (3, 1))
        # time.sleep(1)
        
        
        #pygame.display.update()

        # Flip the display
        #pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()



if __name__ == '__main__':
    main()