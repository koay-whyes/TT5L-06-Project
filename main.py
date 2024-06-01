import pygame, random, os, menubutton,csv
from pygame import mixer
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
# define game variables
GRAVITY = 0.75
ROWS = 20
COLS = 200
TILE_SIZE = HEIGHT // ROWS
TILE_TYPES = 29
SCROLL_THRESH = 400
screen_scroll = 0
bg_scroll = 0
level = 1
cheezy = 0


# define player action variables
moving_left = False
moving_right = False 
shoot = False 

# load images
bg_img = pygame.image.load('img/level_1.png').convert_alpha()


# store tiles in a list
img_list = []
for x in range(TILE_TYPES):
	img = pygame.image.load(f'img/Interactive Elements/tiles/{x}.png')
	img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
	img_list.append(img)
# Pepperoni (bullet)

pepperoni_img = pygame.image.load('img/icons/pepperoni.png').convert_alpha()
#pick up boxes
health_box_img = pygame.image.load('img/Interactive Elements/tiles/28.png').convert_alpha()
ammo_box_img = pygame.image.load('img/Interactive Elements/tiles/27.png').convert_alpha()
cheezy_img = pygame.image.load('img/Interactive Elements/tiles/21.png').convert_alpha()
item_boxes = {
	'Health'	: health_box_img,
	'Ammo'		: ammo_box_img
}

# define colours
BG = (252,244,163)
WOOD_BROWN = (193, 154, 107) 
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
	
#define font
font = pygame.font.SysFont('Futura', 30)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_bg():
    screen.fill(BG)
    # scrolling
    width =  bg_img.get_width()
    for x in range(5):
    # bg_img = pygame.image.load('img/level_1.png').convert_alpha()
        screen.blit(bg_img, ((x * width) - bg_scroll, 0))

# fixed the bullet-character gap problem
def custom_collision(character, pepperoni_group):
    # Calculate the centers
    pepperoni_center = pepperoni_group.rect.center
    character_center = character.rect.center
        
    # Define a distance threshold, e.g., 10 pixels towards the center
    distance_threshold = 10
        
    # Check if the bullet is within the threshold distance to the character's center
    return pygame.math.Vector2(pepperoni_center).distance_to(character_center) <= distance_threshold

#Main Menu images
title_img = pygame.image.load("img/title.png").convert_alpha()
settings_img = pygame.image.load("img/settings_button.png").convert_alpha()
play_img = pygame.image.load("img/play_button.png").convert_alpha()
exit_img=pygame.image.load("img/exit_button.png").convert_alpha()
menu_background_img=pygame.image.load("img/menu_background.png")

#Settings Images
soundon_img = pygame.image.load("img/soundon_button.png").convert_alpha()
soundoff_img = pygame.image.load("img/soundoff_button.png").convert_alpha()
back_img = pygame.image.load("img/back_button.png").convert_alpha()
sfx_img = pygame.image.load("img/sfx_button.png").convert_alpha()
NoSfx_img = pygame.image.load("img/NoSfx_button.png").convert_alpha()
sfx_text_img = pygame.image.load("img/sfx_text.png").convert_alpha()
music_img = pygame.image.load("img/music_text.png").convert_alpha()

#Game img
comic_panel  = pygame.image.load("img/comic_panel.jpeg")
background_img = pygame.image.load("img/background.jpg")


#Pause Menu
pause_img = pygame.image.load("img/pause_button.png").convert_alpha()
restart_img = pygame.image.load("img/restart_button.png").convert_alpha()
menu_img = pygame.image.load("img/menu_button.png").convert_alpha()
resume_img = pygame.image.load("img/resume_button.png").convert_alpha()
warning_img = pygame.image.load("img/warning.png").convert_alpha()
warning_scaled_img=pygame.transform.scale(warning_img,(320,320))
tick_img = pygame.image.load("img/tick_button.png").convert_alpha()
x_img = pygame.image.load("img/x_button.png").convert_alpha()
next_img = pygame.image.load("img/next_button.png").convert_alpha()

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


#reset level
def reset_level():
    global player, enemy
    pepperoni_group.empty()

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
            # update background
            draw_bg()
            #draw world map
            world.draw()
            #show player health
            health_bar.draw(player.health)
            #show ammo
            draw_text('PEPPERONI: ', font, WOOD_BROWN, 10, 45) 
            for x in range(player.ammo):
                screen.blit(pepperoni_img, (125 + (x * 10), 40))
            #show cheezy
            draw_text(f'CHEEZY:', font, WOOD_BROWN, 10, 65)
            for x in range(player.cheezy):
                screen.blit(cheezy_img, (100 + (x * 25), 65))
                
            player.update() 
            player.draw()

            for enemy in enemy_group:
            # takes screen scroll as value
                enemy.ai(screen_scroll)
                enemy.update()
                enemy.draw()

            # update and draw groups
            pepperoni_group.update()
            item_box_group.update(screen_scroll)
            decoration_group.update(screen_scroll)
            threat_group.update(screen_scroll)
            exit_group.update(screen_scroll)

            pepperoni_group.draw(screen)
            item_box_group.draw(screen)
            decoration_group.draw(screen)
            threat_group.draw(screen)
            exit_group.draw(screen)



            # update player actions
            if player.alive: 
                # shoot pepperoni
                if shoot:
                    player.shoot()
                if player.in_air:
                    player.update_action(2) # 2: jump
                elif moving_left or moving_right:
                    player.update_action(1) # 1: run/roll
                else:
                    player.update_action(0) # index 0: idle
                screen_scroll = player.move(moving_left, moving_right) # follows player speed
                bg_scroll -= screen_scroll # cumulative

                max_scroll = (world.level_length * TILE_SIZE) - SCREEN_WIDTH
                if bg_scroll < 0:
                    bg_scroll = 0
                elif bg_scroll > max_scroll:
                    bg_scroll = max_scroll

                # not calling enemy.move()
            

            #Pause Menu
            if pause_button.draw(screen):
                pause_menu = True
            if pause_menu==True:
                screen.fill(WOOD_BROWN)
                #Continue
                if resume_button.draw(screen):
                    pause_menu=False
                #Restart Level
                if restart_button.draw(screen):
                    pause_menu=False
                    reset_level()
                if menu_button.draw(screen):
                    warning=True
                if warning == True: 
                    screen.blit(warning_scaled_img, (370,90))
                    if tick_button.draw(screen):
                        main_menu=True
                        pause_menu=False
                        settings=False
                        warning=False
                        reset_level()
                    elif x_button.draw(screen):
                        pause_menu=True
                        warning=False

    pygame.display.update() 

pygame.quit()
