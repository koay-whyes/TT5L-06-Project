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
TILE_TYPES = 21
level = 1

#music
MainMusic = pygame.mixer.Sound("bgm.mp3") 
StoryMusic = pygame.mixer.Sound("sad_bgm.mp3")
GameOverMusic = pygame.mixer.Sound("game_over_bgm.mp3")

main_channel = pygame.mixer.Channel(1)
story_channel = pygame.mixer.Channel(2)
game_over_channel = pygame.mixer.Channel(3)

main_channel.play(pygame.mixer.Sound(MainMusic), loops=-1, fade_ms=1000)
story_channel.play(pygame.mixer.Sound(StoryMusic), loops=-1, fade_ms=1000)
game_over_channel.play(pygame.mixer.Sound(GameOverMusic), loops=-1, fade_ms=10)

# define player action variables
moving_left = False
moving_right = False 
shoot = False 

# load img
# store tiles in a list
img_list = []
for x in range(TILE_TYPES):
	img = pygame.image.load(f'img/Tile/{x}.png')
	img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
	img_list.append(img)
# Pepperoni (bullet)

pepperoni_img = pygame.image.load('img/icons/pepperoni.png').convert_alpha()
#pick up boxes
health_box_img = pygame.image.load('img/icons/health_box.png').convert_alpha()
ammo_box_img = pygame.image.load('img/icons/ammo_box.png').convert_alpha()
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
    """    bg_img = pygame.image.load('img/level_1.png').convert_alpha()
    screen.blit(bg_img,(1000,500) )"""

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
full_scren_img = pygame.image.load("img/full_screen.png").convert_alpha()

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
full_screen_button=menubutton.DrawMenu(850,150,full_scren_img,1.5)
    
#reset level
def reset_level():
    global player,enemy,health_bar
    enemy_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()
    pepperoni_group.empty()

    #create empty tile list
    world_data = []
    for row in range(ROWS):
        r = [-1] * COLS
        world_data.append(r)
    #load in level data and create world
    with open(f'level{level}_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                world_data[x][y] = int(tile)
    world = World()
    player, health_bar = world.process_data(world_data)

def game_over():
    game_over_background_img=pygame.image.load("img/game_over_bg.png")
    game_over_restart_img=pygame.image.load("img/game_over_restart.png").convert_alpha()
    game_over_restart_button = menubutton.DrawMenu(440,360,game_over_restart_img,2.5)
    screen.blit(game_over_background_img,(0,0))
    main_channel.pause()
    game_over_channel.unpause()
    if game_over_restart_button.draw(screen):
        reset_level()
        main_channel.unpause()
        game_over_channel.pause()
settings=False
main_menu=True
sound_on=True
sfx=True
pause_menu=False
warning=False
story=False

#story
story_texts = [ 

    "Long ago, all the pizza ingredients lived together in harmony.(PRESS ENTER)",
    "Then, everything changed when the Pineapple attacked.(PRESS ENTER)",
    "Only the pepperoni pizza, Peppy, with its superpizza abilities could stop him.(PRESS ENTER)",
    "He will need the help of the power ups and the cheezys to stand a chance to defeat the Pineapple.",
    "And of course, yours!(PRESS NEXT TO START THE GAME)",
]

story_index = 0


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
            if event.key == pygame.K_a and not pause_menu:
                moving_left = True
            elif event.key == pygame.K_d and not pause_menu:
                moving_right = True
            elif event.key == pygame.K_SPACE and not pause_menu:
                shoot = True
            elif event.key == pygame.K_w and player.alive and not pause_menu:
                player.jump = True
            elif event.key == pygame.K_ESCAPE:
                running = False 
            elif event.key == pygame.K_RETURN:
                story_index = (story_index + 1) % len(story_texts)



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
        game_over_channel.pause()
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
        if full_screen_button.draw(screen):
            screen=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    elif story==True:
        screen.fill(BLACK)
        text = font.render(story_texts[story_index], True, WHITE)
        screen.blit(text, (40, 400))
        if story_index == 4:
            if next_button.draw(screen):
                story=False
                story_channel.pause()
                main_channel.unpause()
    else:
        if not pause_menu:
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
                
            player.update() 
            player.draw()
            for enemy in enemy_group:
                enemy.ai()
                enemy.update()
                enemy.draw()

            # update and draw groups
            pepperoni_group.update()
            item_box_group.update()
            decoration_group.update()
            water_group.update()
            exit_group.update()

            pepperoni_group.draw(screen)
            item_box_group.draw(screen)
            decoration_group.draw(screen)
            water_group.draw(screen)
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
                player.move(moving_left, moving_right)
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
        if player.alive==False:
            game_over()

    pygame.display.update() 

pygame.quit()
