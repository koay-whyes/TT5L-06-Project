import pygame
import random
import os

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

#import images from folder
image_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
title_path = os.path.join(image_folder, "title.png")

#main menu design
class DrawMenu():
    def __init__(self,x, y, image,scale):
        self.image=image
        self.rect = self.image.get_rect()
        self.rect.topleft=(x,y)
        
    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))
title_img = pygame.image.load(title_path).convert_alpha()
title=DrawMenu(100,200,title_img)

def main_menu():
    screen.fill((169, 29, 29))

    title.draw()

# Game loop
running = True 
while running: 
    clock.tick(FPS)
    main_menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update - for sprite to move etc
    all_sprites.update()


    # Draw / render - draw the sprite onto the screen
    #screen.fill(BLACK) 
    all_sprites.draw(screen)

    pygame.display.flip() 

pygame.quit()
