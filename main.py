# Simple pygame program

# Import and initialize the pygame library
import pygame
import time



def main():
    pygame.init()
    LENGTH = 800
    # Set up the drawing window
    screen = pygame.display.set_mode([LENGTH, LENGTH])

    # Run until the user asks to quit
    running = True
    while running:

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the background with white
        screen.fill('white')
        # pygame.display.update()
        # screen.fill('black')
        # pygame.display.update()
        for i in range(0, 8):
            for j in range(0, 8):
                if ((i + j) % 2 == 1):
                    square_dim = LENGTH / 8
                    pygame.draw.rect(screen, 'black', (i * square_dim, j * square_dim, LENGTH / 8, LENGTH / 8))

        # Draw a solid blue circle in the center
        pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

        screen.blit(pygame.image.load('imgs/b_rook.png'), (0, 0))
        pygame.display.update()

        # Flip the display
        #pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()



if __name__ == '__main__':
    main()