import pygame, random, os, menubutton
from pygame import mixer
import mainShoot as MS
pygame.init() 

WIDTH = 1000
HEIGHT = int(WIDTH * 0.5)
 
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

# define player action variables
moving_left = False
moving_right = False 
shoot = False 

#Main Menu images
title_img = pygame.image.load("images/title.png").convert_alpha()
settings_img = pygame.image.load("images/settings_button.png").convert_alpha()
play_img = pygame.image.load("images/play_button.png").convert_alpha()
exit_img=pygame.image.load("images/exit_button.png").convert_alpha()
menu_background_img=pygame.image.load("images/menu_background.png")

#Settings Images
soundon_img = pygame.image.load("images/soundon_button.png").convert_alpha()
soundoff_img = pygame.image.load("images/soundoff_button.png").convert_alpha()
back_img = pygame.image.load("images/back_button.png").convert_alpha()
sfx_img = pygame.image.load("images/sfx_button.png").convert_alpha()
NoSfx_img = pygame.image.load("images/NoSfx_button.png").convert_alpha()
sfx_text_img = pygame.image.load("images/sfx_text.png").convert_alpha()
music_img = pygame.image.load("images/music_text.png").convert_alpha()

#Game Images
comic_panel  = pygame.image.load("images/comic_panel.jpeg")
background_img = pygame.image.load("images/background.jpg")
pepperoni_img = pygame.image.load('images/icons/pepperoni.png').convert_alpha()
#pick up boxes
health_box_img = pygame.image.load('images/icons/health_box.png').convert_alpha()
ammo_box_img = pygame.image.load('images/icons/ammo_box.png').convert_alpha()
item_boxes = {
	'Health'	: health_box_img,
	'Ammo'		: ammo_box_img
}

#Pause Menu
pause_img = pygame.image.load("images/pause_button.png").convert_alpha()
restart_img = pygame.image.load("images/restart_button.png").convert_alpha()
menu_img = pygame.image.load("images/menu_button.png").convert_alpha()
resume_img = pygame.image.load("images/resume_button.png").convert_alpha()
warning_img = pygame.image.load("images/warning.png").convert_alpha()
warning_scaled_img=pygame.transform.scale(warning_img,(320,320))
tick_img = pygame.image.load("images/tick_button.png").convert_alpha()
x_img = pygame.image.load("images/x_button.png").convert_alpha()
next_img = pygame.image.load("images/next_button.png").convert_alpha()

#text
title=menubutton.DrawMenu(320,0,title_img,6)
sfx_text=menubutton.DrawMenu(50,100,sfx_text_img,5)
music_text=menubutton.DrawMenu(50,250,music_img,5)

#create button
play_button=menubutton.DrawMenu(440,200,play_img,2.5)
settings_button=menubutton.DrawMenu(440,280,settings_img,2.5)
exit_button=menubutton.DrawMenu(440,360,exit_img,2.5)
sound_button=menubutton.DrawMenu(350,260,soundon_img,3)
back_button=menubutton.DrawMenu(600,280,back_img,2.5)
sfx_button=menubutton.DrawMenu(350,100,sfx_img,4.5)
pause_button=menubutton.DrawMenu(940,0,pause_img,2)
restart_button=menubutton.DrawMenu(440,100,restart_img,2.5)
menu_button=menubutton.DrawMenu(100,100,menu_img,2.5)
resume_button=menubutton.DrawMenu(780,100,resume_img,2.5)
tick_button=menubutton.DrawMenu(340,290,tick_img,5)
x_button=menubutton.DrawMenu(570,290,x_img,5)
next_button=menubutton.DrawMenu(850,150,next_img,1.5)

# create sprite groups
enemy_group = pygame.sprite.Group()
pepperoni_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()

#temp - create item boxes
item_box = MS.ItemBox('Health', 100, 260)
item_box_group.add(item_box)
item_box = MS.ItemBox('Ammo', 400, 260)
item_box_group.add(item_box)

# create an player instance of the class for player
player = MS.Character("Peppy",200,200,3, 5, 20)
health_bar = MS.HealthBar(10, 10, player.health, player.health)
enemy = MS.Character("Pineapple",500, 200, 3, 2, 20) # change char type later
enemy2 = MS.Character('Pineapple', 300, 200, 3, 2, 20)		
enemy_group.add(enemy)		
enemy_group.add(enemy2)

#reset level
def reset_level():
    global player, enemy, settings , main_menu,pause_menu,warning,story
    settings=False
    main_menu=True
    pause_menu=False
    warning=False
    story=False
    pepperoni_group.empty()
    enemy_group.empty()
    item_box_group.empty()
    item_box = MS.ItemBox('Health', 100, 260)
    item_box_group.add(item_box)
    item_box = MS.ItemBox('Ammo', 400, 260)
    item_box_group.add(item_box)
    player = MS.Character("Peppy",200,200,3, 5, 20)
    health_bar = MS.HealthBar(10, 10, player.health, player.health)
    enemy = MS.Character("Pineapple",500, 200, 3, 2, 20) # change char type later
    enemy2 = MS.Character('Pineapple', 300, 200, 3, 2, 20)		
    enemy_group.add(enemy)		
    enemy_group.add(enemy2)

settings=False
main_menu=True
sound_on=True
sfx=True
pause_menu=False
warning=False
story=False
# Game loop
MainMusic = pygame.mixer.Sound("bgm.mp3") 
StoryMusic = pygame.mixer.Sound("sad_bgm.mp3")

main_channel = pygame.mixer.Channel(1)
story_channel = pygame.mixer.Channel(2)

main_channel.play(pygame.mixer.Sound(MainMusic), loops=-1, fade_ms=1000)
story_channel.play(pygame.mixer.Sound(StoryMusic), loops=-1, fade_ms=1000)

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
    if main_menu==True:
        screen.blit(menu_background_img, (0,0))
        title.draw(screen)
        story_channel.pause()
        if exit_button.draw(screen):
            running=False
        if settings_button.draw(screen):
            main_menu=False
            settings=True
            story=False
        if play_button.draw(screen):
            story=True
            main_menu=False
            story_channel.unpause()
            main_channel.pause()

      
    elif settings==True:
        screen.fill((255, 224, 142))
        sfx_text.draw(screen)
        music_text.draw(screen)
        story_channel.pause()
        main_channel.unpause()
        if back_button.draw(screen):
            main_menu=True
            settings=False
        if sound_button.draw(screen):
            sound_on=not sound_on
            if sound_on:
                sound_button.update_image(soundon_img,3)
                main_channel.play(pygame.mixer.Sound(MainMusic), loops=-1, fade_ms=0)
            else:
                sound_button.update_image(soundoff_img,3)
                main_channel.stop()
        if sfx_button.draw(screen):
                sfx=not sfx
                if sfx:
                    sfx_button.update_image(sfx_img,4.5)
                    pygame.mixer.Channel(0).set_volume(0.5)
                else:
                    sfx_button.update_image(NoSfx_img,4.5)
                    pygame.mixer.Channel(0).set_volume(0)

    elif story==True:
        screen.fill(BLACK)
        screen.blit(comic_panel,(350,0))
        if next_button.draw(screen):
            story=False
            story_channel.pause()
            main_channel.unpause()
    else:
            MS.draw_bg()
            #show player health
            health_bar.draw(player.health)
            #show ammo
            MS.draw_text('AMMO: ', MS.font, WHITE, 10, 35)
            for x in range(player.ammo):
                screen.blit(pepperoni_img, (90 + (x * 10), 40))
                
            player.update() 
            player.draw()

            for enemy in enemy_group:
                enemy.ai()
                enemy.update()
                enemy.draw()
                        # update and draw groups
            pepperoni_group.update()
            pepperoni_group.draw(screen)
            if player.alive:
                # shoot pepperoni
                if shoot:
                    pepperoni = MS.Pepperoni(player.rect.centerx + (0.6 * player.rect.size[0]*player.direction), player.rect.centery, player.direction)
                    pepperoni_group.add(pepperoni)

                if player.in_air:
                    player.update_action(2) # 2: jump
                elif moving_left or moving_right:
                    player.update_action(1) # 1: run/roll
                else:
                    player.update_action(0) # index 0: idle
                player.move(moving_left, moving_right)
                # not calling enemy.move()

            #Pause Menu
            if pause_button.draw(screen):
                pause_menu = True
            if pause_menu==True:
                screen.fill((193, 154, 107))
                #Continue
                if resume_button.draw(screen):
                    pause_menu=False
                #Restart Level
                if restart_button.draw(screen):
                    reset_level()
                    main_menu=False
                if menu_button.draw(screen):
                    warning=True
                if warning == True: 
                    screen.blit(warning_scaled_img, (370,90))
                    if tick_button.draw(screen):
                        reset_level()
                    elif x_button.draw(screen):
                        pause_menu=True
                        warning=False


            
    pygame.display.update() 

pygame.quit()
