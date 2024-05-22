import pygame, random, os, menubutton
from pygame import mixer
import PeppyMovement as PM
import csv
from environment import Environment

pygame.init() 

WIDTH = 1000
HEIGHT = 500
 
# define colors *might split into another file afterwards
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BG = (252,244,163)
WOOD_BROWN = (193, 154, 107) 

# initialize pygame and create window

pygame.mixer.init() 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Peppy the Pizza") # display on top of the window

# set framerate
clock = pygame.time.Clock() 
FPS = 60 
# define game variables
GRAVITY = 0.75
# environment variables
ROWS = 20
COLS = 200
TILE_SIZE = HEIGHT // ROWS
TILE_TYPES = 16
level = 1

# define player action variables
moving_left = False
moving_right = False 
shoot = False 

#Load and play bg music
pygame.mixer.music.load("bg_music.mp3")
#Repeats,when to start playing
pygame.mixer.music.play(-1,0.0)
pygame.mixer.music.set_volume(0.3)

all_sprites = pygame.sprite.Group() 

#Main Menu
title_img = pygame.image.load("images/title.png").convert_alpha()
option_img = pygame.image.load("images/option_button.png").convert_alpha()
play_img = pygame.image.load("images/play_button.png").convert_alpha()
exit_img=pygame.image.load("images/exit_button.png").convert_alpha()
soundon_img = pygame.image.load("images/soundon_button.png").convert_alpha()
soundoff_img = pygame.image.load("images/soundoff_button.png").convert_alpha()
back_img = pygame.image.load("images/back_button.png").convert_alpha()
background_img = pygame.image.load("images/background.jpg")

# load environment images
bg_img = pygame.image.load("resources/Background/Level 1/level_1.png").convert_alpha()
# store tiles in a list 
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'resources/Interactive Elements/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

#create button
title=menubutton.DrawMenu(100,200,title_img,5)
play=menubutton.DrawMenu(334,180,play_img,5)
playinsettings=menubutton.DrawMenu(334,180,play_img,5)
option=menubutton.DrawMenu(334,280,option_img,5)
exit=menubutton.DrawMenu(334,380,exit_img,5)
sound_button=menubutton.DrawMenu(100,200,soundon_img,5)
back=menubutton.DrawMenu(500,280,back_img,5)

# create sprite groups
pepperoni_group = pygame.sprite.Group()

# create an player instance of the class for player
player = PM.Character("Peppy",200,200,3, 5)
enemy = PM.Character("Peppy",430,150,3, 5) # change char type later

def draw_bg():
    screen.fill(BG)
    screen.blit(bg_img, (0,0))

# create empty tile list
environment_data = []
# -1 means empty
for row in range(ROWS):
    r = [-1] * COLS
    environment_data.append(r)

# load in level data and create environment
# loading using csv
with open(f'level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    # getting individual values
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            environment_data[x][y] = int(tile)

# process data
environment = Environment(img_list)
environment.process_data(environment_data)

settings=False
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
        # keyboard presses (KEYDOWN)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            elif event.key == pygame.K_d:
                moving_right = True
            elif event.key == pygame.K_SPACE:
                shoot = True
            elif event.key == pygame.K_w and player.alive:
                player.jump = True
            elif event.key == pygame.K_ESCAPE:
                running = False 

        # keyboard button released (KEYUP)
        elif event.type == pygame.KEYUP: 
            if event.key == pygame.K_a :
                moving_left = False 
            elif event.key == pygame.K_d:
                moving_right = False 
            elif event.key == pygame.K_SPACE:
                shoot = False 

    #Main Menu
    if main_menu:
        screen.fill((169, 29, 29))
        title.draw(screen)

        if exit.draw(screen):
            print("exit button pressed")
            running=False
        elif play.draw(screen):
            print("play button pressed")
            main_menu=False
            settings=False
        elif option.draw(screen):
            print("option button pressed")
            settings=True    
            main_menu=False
            
    elif settings==True:
        screen.fill(BLACK)
        if back.draw(screen): 
            main_menu=True   
            settings=False
        elif sound_button.draw(screen):
            sound_on=not sound_on
            if sound_on:
                sound_button.update_image(soundon_img,5)
                pygame.mixer.music.play(-1)
            else:
                sound_button.update_image(soundoff_img,5)
                pygame.mixer.music.pause()
    else:
            draw_bg()
            environment.draw(screen)
            player.update_animation()
            player.draw()
            enemy.draw()

            # update and draw groups
            pepperoni_group.update()
            pepperoni_group.draw(screen)
            if player.alive:
                # shoot pepperoni
                if shoot:
                    pepperoni = PM.Pepperoni(player.rect.centerx + (0.6 * player.rect.size[0]*player.direction), player.rect.centery, player.direction)
                    pepperoni_group.add(pepperoni)

                if player.in_air:
                    player.update_action(2) # 2: jump
                elif moving_left or moving_right:
                    player.update_action(1) # 1: run/roll
                else:
                    player.update_action(0) # index 0: idle
                player.move(moving_left, moving_right)
                # not calling enemy.move()
        
    pygame.display.update() 

pygame.quit()
