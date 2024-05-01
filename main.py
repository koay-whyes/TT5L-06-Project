import pygame, random, os, menubutton
from pygame import mixer

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

#Load and play bg music
pygame.mixer.music.load("bg_music.mp3")
#Repeats,when to start playing
pygame.mixer.music.play(-1,0.0)
pygame.mixer.music.set_volume(0.3)

all_sprites = pygame.sprite.Group() 


#import images from folder
image_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
title_path = os.path.join(image_folder, "title.png")
play_path = os.path.join(image_folder,"play_button.png")
option_path=os.path.join(image_folder,"option_button.png")
exit_path=os.path.join(image_folder,"exit_button.png")
soundon_path = os.path.join(image_folder, "soundon_button.png")
soundoff_path = os.path.join(image_folder, "soundoff_button.png")
back_path= os.path.join(image_folder, "back_button.png")
#load images
title_img = pygame.image.load(title_path).convert_alpha()
play_img = pygame.image.load(play_path).convert_alpha()
option_img = pygame.image.load(option_path).convert_alpha()
exit_img=pygame.image.load(exit_path).convert_alpha()
soundon_img = pygame.image.load(soundon_path).convert_alpha()
soundoff_img = pygame.image.load(soundoff_path).convert_alpha()
back_img = pygame.image.load(back_path).convert_alpha()
#create button
title=menubutton.DrawMenu(100,200,title_img,5)
play=menubutton.DrawMenu(334,180,play_img,5)
option=menubutton.DrawMenu(334,280,option_img,5)
exit=menubutton.DrawMenu(334,380,exit_img,5)
sound_button=menubutton.DrawMenu(100,200,soundon_img,5)
back=menubutton.DrawMenu(500,280,back_img,5)

main_menu=True
sound_on=True
# Game loop
running = True 
while running: 
    clock.tick(FPS)
    #click X on the right top to close the program
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Main Menu
    if main_menu:
        screen.fill((169, 29, 29))
        title.draw(screen)
        if exit.draw(screen):
            running=False
        if play.draw(screen):
            print("START")
            # Update - for sprite to move etc
            all_sprites.update()
            # Draw / render - draw the sprite onto the screen
            all_sprites.draw(screen)
        if option.draw(screen):
            main_menu=False
            screen.fill(BLACK)

            

    else:
        if back.draw(screen):
            main_menu=True
        if sound_button.draw(screen):
            sound_on=not sound_on
            if sound_on:
                sound_button.update_image(soundon_img,5)
                pygame.mixer.music.play(-1)
            else:
                sound_button.update_image(soundoff_img,5)
                pygame.mixer.music.pause()

    pygame.display.flip()
    pygame.display.update() 

pygame.quit()
