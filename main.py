import pygame, random, os, menubutton,csv
from pygame import mixer
import mainShoot as MS
from mainShoot import *
pygame.init() 

WIDTH = 1000
HEIGHT = 500

# initialize pygame and create window

pygame.mixer.init() 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Peppy the Pizza") # display on top of the window

# set framerate
clock = pygame.time.Clock() 
FPS = 60 

#music

MainMusic = pygame.mixer.Sound("bgm.mp3") 
#StoryMusic = pygame.mixer.Sound("sad_bgm.mp3")
#GameOverMusic = pygame.mixer.Sound("game_over_bgm.mp3")
VictoryMusic= pygame.mixer.Sound("victory_bgm.mp3") 
StatsMusic=pygame.mixer.Sound("stats_bgm.mp3")

main_channel = pygame.mixer.Channel(1)
#story_channel = pygame.mixer.Channel(2)
#game_over_channel = pygame.mixer.Channel(3)
victory_channel = pygame.mixer.Channel(4)
stats_channel=pygame.mixer.Channel(5)

main_channel.play(pygame.mixer.Sound(MainMusic), loops=-1, fade_ms=1000)
#story_channel.play(pygame.mixer.Sound(StoryMusic), loops=-1, fade_ms=1000)
#game_over_channel.play(pygame.mixer.Sound(GameOverMusic), loops=-1, fade_ms=10)
victory_channel.play(pygame.mixer.Sound(VictoryMusic), loops=-1, fade_ms=1000)
stats_channel.play(pygame.mixer.Sound(StatsMusic), loops=-1, fade_ms=1000)

victory_channel.pause()
stats_channel.pause()
# define colours
BG = (252,244,163)
WOOD_BROWN = (193, 154, 107) 
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

#Victory
victory_background_img=pygame.image.load("img/victory_bg.png")
victory_mainmenu_img=pygame.image.load("img/victory_house.png").convert_alpha()
victory_next_img=pygame.image.load("img/victory_next.png").convert_alpha()
victory_settings_img=pygame.image.load("img/victory_settings.png").convert_alpha()
stats_img=pygame.image.load("img/victory_stats.png").convert_alpha()

#Stats
#stats_background_img=pygame.image.load("img/stats_background.png")
stats_return_img=pygame.image.load("img/stats_return.png").convert_alpha()
stats_add_img=pygame.image.load("img/stats_add_button.png").convert_alpha()
attack_stats_img=pygame.image.load("img/attack_stats.png").convert_alpha()
defense_stats_img=pygame.image.load("img/defense_stats.png").convert_alpha()
health_stats_img=pygame.image.load("img/health_stats.png").convert_alpha()
pizza_stats1_img=pygame.image.load("img/pizza_stats1.png").convert_alpha()
pizza_stats2_img=pygame.image.load("img/pizza_stats2.png").convert_alpha()
pizza_stats3_img=pygame.image.load("img/pizza_stats3.png").convert_alpha()


#Victory Menu Button
victory_mainmenu_button=menubutton.DrawMenu(620,350,victory_mainmenu_img,1.5)
victory_settings_button=menubutton.DrawMenu(725,350,victory_settings_img,1.5)
victory_next_button= menubutton.DrawMenu(620,120,victory_next_img,3.0)
stats_button=menubutton.DrawMenu(620,210,stats_img,3.0)

#Stats Menu button
stats_return_button=menubutton.DrawMenu(620,210,stats_img,3.0)
stats_add_button=menubutton.DrawMenu(620,210,stats_img,3.0)
attack_stats_button=menubutton.DrawMenu(620,210,stats_img,3.0)
defense_stats_button=menubutton.DrawMenu(620,210,stats_img,3.0)
health_stats_button=menubutton.DrawMenu(620,210,stats_img,3.0)
pizza_stats1_button=menubutton.DrawMenu(620,210,stats_img,3.0)
pizza_stats2_button=menubutton.DrawMenu(620,210,stats_img,3.0)
pizza_stats3_button=menubutton.DrawMenu(620,210,stats_img,3.0)
    

victory=True
stats=False
# Game loop

running = True 
while running: 
    clock.tick(FPS)
    #click X on the right top to close the program
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #Victory Menu
    if victory:
        main_channel.pause()
        victory_channel.unpause()
        screen.blit(victory_background_img,(0,0))
        victory_mainmenu_button.draw(screen)
        victory_settings_button.draw(screen)
        victory_next_button.draw(screen)
        if stats_button.draw(screen):
            stats=True
            victory=False
        if stats==True:
            stats_channel.unpause()
            screen.fill(WOOD_BROWN)
            


    pygame.display.update() 

pygame.quit()
