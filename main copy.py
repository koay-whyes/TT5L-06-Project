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
victory_background_img=pygame.image.load("img/victory/victory_bg.png")
victory_mainmenu_img=pygame.image.load("img/victory/victory_house.png").convert_alpha()
victory_next_img=pygame.image.load("img/victory/victory_next.png").convert_alpha()
victory_settings_img=pygame.image.load("img/victory/victory_settings.png").convert_alpha()
stats_img=pygame.image.load("img/victory/victory_stats.png").convert_alpha()

#Stats
#stats_background_img=pygame.image.load("img/stats_background.png")
stats_return_img=pygame.image.load("img/victory/stats_return.png").convert_alpha()
stats_add_img=pygame.image.load("img/victory/stats_add_button.png").convert_alpha()
attack_stats_img=pygame.image.load("img/victory/attack_stats.png").convert_alpha()
defense_stats_img=pygame.image.load("img/victory/defense_stats.png").convert_alpha()
health_stats_img=pygame.image.load("img/victory/health_stats.png").convert_alpha()
pizza_stats0_img=pygame.image.load("img/victory/pizza_stats0.png").convert_alpha()
pizza_stats1_img=pygame.image.load("img/victory/pizza_stats1.png").convert_alpha()
pizza_stats2_img=pygame.image.load("img/victory/pizza_stats2.png").convert_alpha()
pizza_stats3_img=pygame.image.load("img/victory/pizza_stats3.png").convert_alpha()


#Victory Menu Button
victory_mainmenu_button=menubutton.DrawMenu(620,350,victory_mainmenu_img,1.5)
victory_settings_button=menubutton.DrawMenu(725,350,victory_settings_img,1.5)
victory_next_button= menubutton.DrawMenu(620,120,victory_next_img,3.0)
stats_button=menubutton.DrawMenu(620,210,stats_img,3.0)

#Stats Menu button
stats_return_button=menubutton.DrawMenu(800,380,stats_return_img,2.5)
stats_add_attack_button=menubutton.DrawMenu(200,250,stats_add_img,2.0)
stats_add_defense_button=menubutton.DrawMenu(500,50,stats_add_img,2.0)
stats_add_health_button=menubutton.DrawMenu(800,250,stats_add_img,2.0)
attack_stats_button=menubutton.DrawMenu(100,230,attack_stats_img,3.0)
defense_stats_button=menubutton.DrawMenu(400,10,defense_stats_img,4.0)
health_stats_button=menubutton.DrawMenu(680,200,health_stats_img,4.5)
#Stats Menu images
pizza_stats0=menubutton.DrawMenu(350,150,pizza_stats0_img,10.0)
pizza_stats1=menubutton.DrawMenu(350,150,pizza_stats1_img,10.0)
pizza_stats2=menubutton.DrawMenu(350,150,pizza_stats2_img,10.0)
pizza_stats3=menubutton.DrawMenu(350,150,pizza_stats3_img,10.0)
    

victory=True
stats=False
cheezy=0
attack_level=0
defense_level=0
health_level=0

pizza_stats_imgs = [pizza_stats0_img, pizza_stats1_img, pizza_stats2_img, pizza_stats3_img]

hovered_images = []
for level in [attack_level, defense_level, health_level]:
    if level == 0:
        hovered_images.append(pizza_stats0_img)
    else:
        hovered_images.append(pizza_stats_imgs[level])

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
    elif stats==True:
        victory_channel.pause()
        stats_channel.unpause()
        screen.fill((255, 224, 130))
        pizza_stats0.draw(screen)
        attack_stats_button.draw(screen)
        defense_stats_button.draw(screen)
        health_stats_button.draw(screen)
        if stats_return_button.draw(screen):
            victory=True
            stats=False
            stats_channel.pause()

        elif stats_add_attack_button.draw(screen):
            #attack+=1
            #cheezy-=1
            attack_level+=1
        if stats_add_defense_button.draw(screen):
            #defense+=1
            #cheezy-=1
            defense_level+=1
        if stats_add_health_button.draw(screen):
            #health+=1
            #cheezy-=1
            health_level+=1
    pizza_attack_stats_dict = {1: pizza_stats1, 2: pizza_stats2, 3: pizza_stats3}
    if attack_level in pizza_attack_stats_dict:
        pizza_attack_stats_dict[attack_level].draw(screen)
    else:
        if attack_level >= 4:
            pizza_stats3.draw(screen)
            print("You have reached the maximum level")

    pizza_defense_stats_dict = {1: pizza_stats1, 2: pizza_stats2, 3: pizza_stats3}
    if defense_level in pizza_defense_stats_dict:
        pizza_defense_stats_dict[defense_level].draw(screen)
    else:
        if defense_level >= 4:
            pizza_stats3.draw(screen)
            print("You have reached the maximum level")

    pizza_health_stats_dict = {1: pizza_stats1, 2: pizza_stats2, 3: pizza_stats3}
    if health_level in pizza_health_stats_dict:
        pizza_health_stats_dict[health_level].draw(screen)
    else:
        if health_level >= 4:
            pizza_stats3.draw(screen)
            print("You have reached the maximum level")



    pygame.display.update() 

pygame.quit()
