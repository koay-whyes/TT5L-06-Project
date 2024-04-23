import pygame
import random

WIDTH = 960
HEIGHT = 540
FPS = 30  

# define colors *might split into another file afterwards
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# initialize pygame and create window
pygame.init() 
pygame.mixer.init() 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Peppy the Pizza") # display on top of the window
clock = pygame.time.Clock() 

all_sprites = pygame.sprite.Group() 

# Game loop
running = True 
while running: 
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update - for sprite to move etc
    all_sprites.update()


    # Draw / render - draw the sprite onto the screen
    screen.fill(BLACK) 
    all_sprites.draw(screen)

    pygame.display.flip() 

pygame.quit()
