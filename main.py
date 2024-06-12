import pygame, random, os, menubutton,csv
from pygame import mixer
from mainShoot import *
import mainShoot as MS
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
level = 1


#music
MainMusic = pygame.mixer.Sound("bgm.mp3") 
StoryMusic = pygame.mixer.Sound("sad_bgm.mp3")
GameOverMusic = pygame.mixer.Sound("game_over_bgm.mp3")
VictoryMusic= pygame.mixer.Sound("victory_bgm.mp3") 
StatsMusic=pygame.mixer.Sound("stats_bgm.mp3")

main_channel = pygame.mixer.Channel(1)
story_channel = pygame.mixer.Channel(2)
game_over_channel = pygame.mixer.Channel(3)
victory_channel = pygame.mixer.Channel(4)
stats_channel=pygame.mixer.Channel(5)

main_channel.play(pygame.mixer.Sound(MainMusic), loops=-1, fade_ms=1000)
story_channel.play(pygame.mixer.Sound(StoryMusic), loops=-1, fade_ms=1000)
game_over_channel.play(pygame.mixer.Sound(GameOverMusic), loops=-1, fade_ms=10)
victory_channel.play(pygame.mixer.Sound(VictoryMusic), loops=-1, fade_ms=1000)
stats_channel.play(pygame.mixer.Sound(StatsMusic), loops=-1, fade_ms=1000)

victory_channel.pause()
stats_channel.pause()
# define player action variables
moving_left = False
moving_right = False 
shoot = False 
dash = False

# load img
bg_imgs = {
    1: pygame.image.load("img/level_1.png").convert_alpha(),
    2: pygame.image.load("img/level_2.png").convert_alpha(),
    3: pygame.image.load("img/level_1.png").convert_alpha()
}


def draw_bg():
    screen.fill(BG)
    # scrolling
    bg_img = bg_imgs.get(level % len(bg_imgs), bg_imgs[1])
    width =  bg_img.get_width()
    for x in range(5):
    # bg_img = pygame.image.load('img/level_1.png').convert_alpha()
        screen.blit(bg_img, ((x * width) - bg_scroll, 0))   


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

#Game img
story_image = pygame.image.load("img/story/story.png")


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

cheezy_warning_img=pygame.image.load("img/victory/cheezy_warning.png").convert_alpha()
maximum_level_warning_img=pygame.image.load("img/victory/maximum_level_warning.png").convert_alpha()

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
next_button=menubutton.DrawMenu(900,380,next_img,1.5)
full_screen_button=menubutton.DrawMenu(850,150,full_scren_img,1.5)

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
cheezy_warning=menubutton.DrawMenu(350,150,cheezy_warning_img,4.5)
maximum_level_warning=menubutton.DrawMenu(350,150,maximum_level_warning_img,4.5)
#Stats Menu images
pizza_stats0=menubutton.DrawMenu(350,150,pizza_stats0_img,10.0)
pizza_stats1=menubutton.DrawMenu(350,150,pizza_stats1_img,10.0)
pizza_stats2=menubutton.DrawMenu(350,150,pizza_stats2_img,10.0)
pizza_stats3=menubutton.DrawMenu(350,150,pizza_stats3_img,10.0)

def reset_level():
    # Load new level data
    global player,enemy,health_bar,world_data
    # Reset player and enemy health
    player.health = 120
    for enemy in enemy_group:
        enemy.health = 120
    player.ammo = 20
    enemy_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    threat_group.empty()
    exit_group.empty()
    pepperoni_group.empty()
    MS.world_data.clear()
    MS.world.obstacle_list.clear()
    world_data = []
    for row in range(ROWS):
        r = [-1] * COLS
        world_data.append(r)
    with open(f'level{level}_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                world_data[x][y] = int(tile)
    MS.world = MS.World()
    MS.world.process_data(world_data, MS.level)
    MS.player.rect.center = (player.rect.centerx,player.rect.centery)
    MS.screen_scroll = 0
    MS.bg_scroll =0
    MS.player.rect.center = (100,100)
    for enemy in enemy_group:
        enemy.rect.center = (enemy.rect.centerx,enemy.rect.centery)



'''
#reset level
def reset_level():
    global player,enemy,health_bar,world_data
    enemy_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    threat_group.empty()
    exit_group.empty()
    pepperoni_group.empty()
    MS.player.health = 120
    MS.player.ammo = 20 
    MS.bg_scroll=0
    MS.screen_scroll=0
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
    player, health_bar = world.process_data(world_data, level)
    MS.player.rect.center = (player.rect.centerx,player.rect.centery)
'''
def game_over():
    game_over_background_img=pygame.image.load("img/game_over_bg.png")
    game_over_restart_img=pygame.image.load("img/game_over_restart.png").convert_alpha()
    game_over_restart_button = menubutton.DrawMenu(410,360,game_over_restart_img,2.5)
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
victory=False
stats=False
start_time = pygame.time.get_ticks()
warning_cheezy_visible = False
maximum_level_visible=False
back_to = None
story_index = 0
attack_level=0
health_level=0
#story
story_texts = [ 
    "Long ago, all the pizza ingredients lived happily together in harmony. (PRESS ENTER)",

    "Out of a sudden, the pineapple turned evil, and no one knew why.",

    "Only Peppy, the pepperoni pizza with superpizza abilities, could stop the Pineapple.",

    "But Peppy will need the help of the cheezys to stand a chance to defeat the Pineapple.",

    "Can you help Peppy find out what happened?(PRESS NEXT TO START)",
]


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


            # dash
            if event.key == pygame.K_j and not pause_menu:
                dash = True 

        # keyboard button released (KEYUP)
        elif event.type == pygame.KEYUP: 
            if event.key == pygame.K_a :
                moving_left = False 
            elif event.key == pygame.K_d:
                moving_right = False 
            elif event.key == pygame.K_SPACE:
                shoot = False 
            elif event.key == pygame.K_j:
                dash = False

    #Main Menu
    if main_menu==True:
        screen.blit(menu_background_img, (0,0))
        title.draw(screen)
        story_channel.pause()
        game_over_channel.pause()
        victory=False
        if exit_button.draw(screen):
            running=False
        if settings_button.draw(screen):
            settings=True
            back_to = "main_menu"
            main_menu=False
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
        stats_channel.pause()
        if back_button.draw(screen):
            if back_to == "victory":
                victory=True
                settings=False
            elif back_to == "main_menu":
                main_menu=True
                settings=False
            back_to = None
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
                    pygame.mixer.Channel(0).set_volume(1.0)
                else:
                    sfx_button.update_image(NoSfx_img,4.5)
                    pygame.mixer.Channel(0).set_volume(0)
        if full_screen_button.draw(screen):
            screen=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    elif story==True:
        screen.fill(BLACK)
        text = font.render(story_texts[story_index], True, WHITE)
        screen.blit(story_image,(0,0))
        screen.blit(text, (40, 460))
        victory=False
        stats=False
        if next_button.draw(screen):
            story=False
            main_menu=False
            story_channel.pause()
            main_channel.unpause()

    #Victory Menu
    elif victory==True:
        main_channel.pause()
        victory_channel.unpause()
        screen.blit(victory_background_img,(0,0))
        if victory_mainmenu_button.draw(screen):
            main_menu=True
            victory=False
            main_channel.unpause()
            victory_channel.pause()
        if victory_settings_button.draw(screen):
            settings=True
            main_channel.unpause()
            victory_channel.pause()
            back_to = "victory"
            victory=True
        if victory_next_button.draw(screen):
            level_complete=True
            victory=False
            main_channel.unpause()
            victory_channel.pause()
        if stats_button.draw(screen):
            stats=True
            victory=False

    elif stats==True:
        victory_channel.pause()
        stats_channel.unpause()
        main_channel.pause()
        screen.fill((255, 224, 130))
        attack_stats_button.draw(screen)
        defense_stats_button.draw(screen)
        health_stats_button.draw(screen)
        pizza_stats0.draw(screen)
        pizza_attack_stats_dict = {1: pizza_stats1, 2: pizza_stats2, 3: pizza_stats3}
        pizza_defense_stats_dict = {1: pizza_stats1, 2: pizza_stats2, 3: pizza_stats3}
        pizza_health_stats_dict = {1: pizza_stats1, 2: pizza_stats2, 3: pizza_stats3}      
        if stats_add_attack_button.draw(screen):
            if attack_level==3:
                maximum_level_visible=True
                start_time = pygame.time.get_ticks()
            else:
                if MS.player.cheezy!=0:
                    MS.player.cheezy-=1
                    attack_level+=1
                    for enemy in enemy_group:
                        enemy.health-=20
                    print(f"attack_level:{attack_level}")
                    print(f"cheezy:{MS.player.cheezy}")
                    print(f"enemy health:{enemy.health}")
                else:
                    warning_cheezy_visible=True
                    start_time = pygame.time.get_ticks()
        if stats_add_defense_button.draw(screen):
            if MS.defense_level==3:
                maximum_level_visible=True
                start_time = pygame.time.get_ticks()
            else:
                if MS.player.cheezy!=0:
                    MS.player.cheezy-=1
                    MS.defense_level+=1
                    print(f"defense_level:{MS.defense_level}")
                    print(f"cheezy:{MS.player.cheezy}")
                else:
                    warning_cheezy_visible=True
                    start_time = pygame.time.get_ticks()
        if stats_add_health_button.draw(screen):
            if health_level==3:
                maximum_level_visible=True
                start_time = pygame.time.get_ticks()
            else:
                if MS.player.cheezy!=0:
                    MS.player.cheezy-=1
                    health_level+=1
                    player.health+=15
                    print(f"health_level:{health_level}")
                    print(f"cheezy:{MS.player.cheezy}")
                    print(f"player health:{player.health}")
                else:
                    warning_cheezy_visible=True
                    start_time = pygame.time.get_ticks()
  
        if attack_level in pizza_attack_stats_dict:
            pizza_attack_stats_dict[attack_level].draw(screen)
        if defense_level in pizza_defense_stats_dict:
            pizza_defense_stats_dict[defense_level].draw(screen)
            if defense_level >= 4:
                pizza_stats3.draw(screen)
                print("You have reached the maximum level")
        if health_level in pizza_health_stats_dict:
            pizza_health_stats_dict[health_level].draw(screen)
            if health_level >= 4:
                pizza_stats3.draw(screen)
                print("You have reached the maximum level")
        else:
            if (attack_level or defense_level or health_level)>= 4:
                pizza_stats3.draw(screen)
                print("You have reached the maximum level")
        if stats_return_button.draw(screen):
            victory=True
            stats=False
            stats_channel.pause()
        if warning_cheezy_visible:
            cheezy_warning.draw(screen)
        if maximum_level_visible:
            maximum_level_warning.draw(screen)
        current_time = pygame.time.get_ticks()
        if current_time - start_time >= 2500:  # 2.5 seconds
            warning_cheezy_visible = False
            maximum_level_visible=False

    else:
        if not pause_menu:
            print(f"{screen_scroll}")
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
            draw_text(f'x{MS.player.cheezy}', font, WOOD_BROWN, 45, 70)
            screen.blit(cheezy_img, (10, 65))
            # for x in range(player.cheezy):
            #   screen.blit(cheezy_img, (100 + (x * 25), 65))


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

            player.update() 
            player.draw()


            # update player actions
            if player.alive:
                # shoot pepperoni
                if shoot:
                    player.shoot()
                    player.update_action(4)
                if player.in_air:
                    player.update_action(2) # 2: jump
                elif moving_left or moving_right:
                    player.update_action(1) # 1: run/roll
                elif dash:
                    player.update_action(1) # can change to other animation 
                else:
                    player.update_action(0) # index 0: idle
                screen_scroll, level_complete = player.move(moving_left, moving_right, dash) # follows player speed # scrolling follows dashing TRUE or FALSE
                bg_scroll -= screen_scroll # cumulative

                # check if player has completed the level
                if level_complete == True:
                    level += 1
                    victory = True
                    reset_level() 
                    # if level <= MAX_LEVELS:
                    if level == 2:
                        #load in level data and create world
                        with open(f'level{level}_data.csv', newline='') as csvfile:
                            reader = csv.reader(csvfile, delimiter=',')
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    world_data[x][y] = int(tile)
                        world = World()
                        player, health_bar = world.process_data(world_data, level)
                max_scroll = (world.level_length * TILE_SIZE) - SCREEN_WIDTH
                if bg_scroll < 0:
                    bg_scroll = 0
                elif bg_scroll > max_scroll:
                    bg_scroll = max_scroll
            else:
                screen_scroll = 0
                
                
                # player.move(moving_left, moving_right, dash)
                
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