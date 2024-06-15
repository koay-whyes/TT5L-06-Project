import pygame, random, os, menubutton,csv
from pygame import mixer
from mainShoot import *
import mainShoot as MS
from pygame.locals import *
from pygame import time
import pymunk
import pymunk.pygame_util

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
screen_scroll = 0
bg_scroll = 0
level = 1
level = 1


#music
MainMusic = pygame.mixer.Sound("bgm/bgm.mp3") 
StoryMusic = pygame.mixer.Sound("bgm/sad_bgm.mp3")
GameOverMusic = pygame.mixer.Sound("bgm/game_over_bgm.mp3")
VictoryMusic= pygame.mixer.Sound("bgm/victory_bgm.mp3") 
StatsMusic=pygame.mixer.Sound("bgm/stats_bgm.mp3")
EndingMusic=pygame.mixer.Sound("bgm/end_bgm.mp3")

#sound effect
jump_fx = pygame.mixer.Sound("sound/jump.mp3")
dead_fx = pygame.mixer.Sound("sound/dead.mp3")

main_channel = pygame.mixer.Channel(1)
story_channel = pygame.mixer.Channel(2)
game_over_channel = pygame.mixer.Channel(3)
victory_channel = pygame.mixer.Channel(4)
stats_channel=pygame.mixer.Channel(5)
end_channel=pygame.mixer.Channel(6)

main_channel.play(pygame.mixer.Sound(MainMusic), loops=-1, fade_ms=1000)
story_channel.play(pygame.mixer.Sound(StoryMusic), loops=-1, fade_ms=1000)
game_over_channel.play(pygame.mixer.Sound(GameOverMusic), loops=-1, fade_ms=10)
victory_channel.play(pygame.mixer.Sound(VictoryMusic), loops=-1, fade_ms=1000)
stats_channel.play(pygame.mixer.Sound(StatsMusic), loops=-1, fade_ms=1000)
end_channel.play(pygame.mixer.Sound(EndingMusic), loops=-1, fade_ms=1000)

victory_channel.pause()
stats_channel.pause()
# define player action variables
moving_left = False
moving_right = False 
shoot = False 
dash = False
def loadify(imgname):
    return  pygame.image.load(imgname).convert_alpha()

# load img
bg_img = pygame.image.load("img/bg.png").convert_alpha()


def draw_bg():
    screen.fill(BG)
    # scrolling
    screen.blit(bg_img, (0 - bg_scroll, 0))   


#Main Menu images
title_img = loadify("img/main_menu/title.png") 
settings_img = loadify("img/main_menu/settings_button.png") 
play_img = loadify("img/main_menu/play_button.png") 
exit_img=loadify("img/main_menu/exit_button.png") 
menu_background_img=loadify("img/main_menu/menu_background.png")

#Settings Images
soundon_img = loadify("img/soundon_button.png") 
soundoff_img = loadify("img/soundoff_button.png") 
back_img = loadify("img/back_button.png") 
sfx_img = loadify("img/sfx_button.png") 
NoSfx_img = loadify("img/NoSfx_button.png") 
sfx_text_img = loadify("img/sfx_text.png") 
music_img = loadify("img/music_text.png") 

#Victory
victory_background_img=loadify("img/victory_bg.png")
victory_mainmenu_img=loadify("img/victory_house.png") 
victory_next_img=loadify("img/victory_next.png") 
victory_settings_img=loadify("img/victory_settings.png") 
stats_img=loadify("img/victory_stats.png") 

#Game OVer
game_over_background_img=loadify("img/game_over_bg.png")
game_over_retry_img=loadify("img/game_over_retry.png") 

#Stats
stats_return_img=loadify("img/stats_return.png") 
stats_add_img=loadify("img/stats_add_button.png") 
attack_stats_img=loadify("img/attack_stats.png") 
defense_stats_img=loadify("img/defense_stats.png") 
health_stats_img=loadify("img/health_stats.png") 
pizza_stats1_img=loadify("img/pizza_stats1.png") 
pizza_stats2_img=loadify("img/pizza_stats2.png") 
pizza_stats3_img=loadify("img/pizza_stats3.png") 

#Story img
story_image = loadify("img/story/story.png")
outro1_image = loadify("img/story/outro1.png")
outro2_image = loadify("img/story/outro2.png")
end_img=loadify("img/end_button.png")

#Victory
victory_background_img=loadify("img/victory/victory_bg.png")
victory_mainmenu_img=loadify("img/victory/victory_house.png") 
victory_next_img=loadify("img/victory/victory_next.png") 
victory_settings_img=loadify("img/victory/victory_settings.png") 
stats_img=loadify("img/victory/victory_stats.png") 

#Stats
stats_return_img=loadify("img/victory/stats_return.png") 
stats_add_img=loadify("img/victory/stats_add_button.png") 
attack_stats_img=loadify("img/victory/attack_stats.png") 
defense_stats_img=loadify("img/victory/defense_stats.png") 
health_stats_img=loadify("img/victory/health_stats.png") 
pizza_stats0_img=loadify("img/victory/pizza_stats0.png") 
pizza_stats1_img=loadify("img/victory/pizza_stats1.png") 
pizza_stats2_img=loadify("img/victory/pizza_stats2.png") 
pizza_stats3_img=loadify("img/victory/pizza_stats3.png") 

cheezy_warning_img=loadify("img/victory/cheezy_warning.png") 
maximum_level_warning_img=loadify("img/victory/maximum_level_warning.png") 

#Pause Menu
pause_img = loadify("img/pause_button.png") 
retry_img = loadify("img/pause/retry_button.png") 
menu_img = loadify("img/pause/menu_button.png") 
resume_img = loadify("img/pause/resume_button.png") 
warning_img = loadify("img/pause/warning.png") 
warning_scaled_img=pygame.transform.scale(warning_img,(320,320))
tick_img = loadify("img/pause/tick_button.png") 
x_img = loadify("img/pause/x_button.png") 
next_img = loadify("img/next_button.png") 
stats_pause_img=loadify("img/pause/stats_pause.png")

#text
title=menubutton.DrawMenu(320,0,title_img,6)
sfx_text=menubutton.DrawMenu(50,100,sfx_text_img,5)
music_text=menubutton.DrawMenu(50,250,music_img,5)


#Main Menu Button
play_button=menubutton.DrawMenu(440,180,play_img,2.5)
settings_button=menubutton.DrawMenu(240,280,settings_img,2.5)
exit_button=menubutton.DrawMenu(640,280,exit_img,2.5)

#settings Button
sound_button=menubutton.DrawMenu(350,260,soundon_img,3)
back_button=menubutton.DrawMenu(600,280,back_img,2.5)
sfx_button=menubutton.DrawMenu(350,100,sfx_img,4.5)

#Pause Button
pause_button=menubutton.DrawMenu(940,0,pause_img,2)
retry_button=menubutton.DrawMenu(240,100,retry_img,2.5)
resume_button=menubutton.DrawMenu(540,100,resume_img,2.5)
menu_button=menubutton.DrawMenu(240,250,menu_img,2.5)
stats_pause_button=menubutton.DrawMenu(540,250,stats_pause_img,2.5)
tick_button=menubutton.DrawMenu(340,290,tick_img,5)
x_button=menubutton.DrawMenu(570,290,x_img,5)
next_button=menubutton.DrawMenu(900,380,next_img,1.5)

#Victory Menu Button
victory_mainmenu_button=menubutton.DrawMenu(620,350,victory_mainmenu_img,1.5)
victory_settings_button=menubutton.DrawMenu(725,350,victory_settings_img,1.5)
victory_next_button= menubutton.DrawMenu(620,120,victory_next_img,3.0)
stats_button=menubutton.DrawMenu(620,210,stats_img,3.0)

#game over button
game_over_retry_button = menubutton.DrawMenu(410,360,game_over_retry_img,2.5)

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

#Ending button
end_button=menubutton.DrawMenu(900,380,end_img,1.5)

settings=False
main_menu=True
sound_on=True
sfx=True
pause_menu=False
warning=False
story=False
victory=False
game_over=False
stats=False
start_game=False
level_complete=False
start_time = pygame.time.get_ticks()
warning_cheezy_visible = False
maximum_level_visible=False
outro=False
credits=False
back_to = None
outro_index=0
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

outro_texts= [
    "Pineapple:(coughing) You... you did it, Peppy. You've defeated me.(PRESS ENTER)",

    "Player: Why, Pineapple? Why did you turn evil?",

    "Pineapple: ...I was once a happy fruit. But everything changed because of one man... Willie.",

    "Player: Willie?",

    "Pineapple: Yes, Willie... He was the one who picked me out of the pizza.", 

    "Pineapple: For too long, we pineapples have been scorned and mistreated by the human race.",
    
    "Pineapple: They treat us like garbage!",

    "Willie: All pineapples belong in the trash!",

    "Pineapple: That's why we fought back, why we sought to eliminate all other toppings!",

    "Pineapple:Only then will those puny humans recognize the respect we deserve.",

    "Pineapple: (weakly) I wanted... I wanted us to be... appreciated...",

    "Player: (softly) It's not too late, Pineapple. We can find a way to change things.",

    "Pineapple: (fading) Too late... for me...",
]

def restart():
    global game_over,start_game,bg_scroll,screen_scroll
    screen.fill(BLACK)
    for enemy in enemy_group:
        enemy.health = 120
    player.ammo = 20
    player.alive=True
    player.health=120
    player.rect.center=(100,100)
    player.ammo = 20
    start_game=True
    game_over = False
    pygame.display.flip()

#Game
def game():
        global pause_menu,main_menu,settings,warning,victory,start_game,level_complete,game_over,back_to,stats,screen_scroll,bg_scroll

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
            #show cheezy
            draw_text(f'x{MS.player.cheezy}', font, WOOD_BROWN, 45, 70)
            screen.blit(cheezy_img, (10, 65))

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
            moving_platform_group.update()

            pepperoni_group.draw(screen)
            item_box_group.draw(screen)
            decoration_group.draw(screen)
            threat_group.draw(screen)
            exit_group.draw(screen)
            moving_platform_group.draw(screen)

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
                player.check_collision(enemy_group)
                bg_scroll -= screen_scroll # cumulative
                max_scroll = (world.level_length * TILE_SIZE) - SCREEN_WIDTH
                if bg_scroll < 0:
                    bg_scroll = 0
                elif bg_scroll > max_scroll:
                    bg_scroll = max_scroll
                if level_complete==True:
                    victory=True
            else:
                game_over=True
                screen_scroll=0
        #Pause Menu
        if pause_button.draw(screen):
            pause_menu = True
        if pause_menu==True:
            screen.fill(WOOD_BROWN)
            #Continue
            if resume_button.draw(screen):
                main_channel.unpause()
                pause_menu=False
            #Restart Level
            if retry_button.draw(screen):
                pause_menu=False
                restart()
            if menu_button.draw(screen):
                warning=True
            if stats_pause_button.draw(screen):
                stats=True
                pause_menu=False
            if warning == True: 
                screen.blit(warning_scaled_img, (370,90))
                if tick_button.draw(screen):
                    main_menu=True
                    pause_menu=False
                    settings=False
                    warning=False
                    restart()
                elif x_button.draw(screen):
                    pause_menu=True
                    warning=False


# Game loop

dead_fx_played = True
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
                jump_fx.play()
            elif event.key == pygame.K_ESCAPE:
                running = False 
            elif event.key == pygame.K_RETURN:
                story_index = (story_index + 1) % len(story_texts)
                outro_index= (outro_index +1) % len(outro_texts)


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
        end_channel.pause()
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

    elif story==True:
        screen.fill(BLACK)
        text = font.render(story_texts[story_index], True, WHITE)
        screen.blit(story_image,(0,0))
        screen.blit(text, (40, 460))
        victory=False
        stats=False
        if next_button.draw(screen):
            start_game=True
            story=False
            main_menu=False
            story_channel.pause()
            main_channel.unpause()

    #Victory Menu
    elif victory==True:
        level_complete=False
        main_channel.pause()
        victory_channel.unpause()
        screen.blit(victory_background_img,(0,0))
        if victory_next_button.draw(screen):
            victory=False
            outro=True
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
    elif outro==True:
        end_channel.unpause()
        victory_channel.pause()
        screen.fill(BLACK)
        text = font.render(outro_texts[outro_index], True, WHITE)
        screen.blit(text, (40, 460))        
        if outro_index>=4:
            screen.blit(outro1_image, (0,0))
        if outro_index>=7:
            screen.blit(outro2_image,(0,0))
        if outro_index==12:
            end_button.draw(screen)
        elif end_button.draw(screen):
            outro=False
            victory=False
            credits=True
    elif credits==True:
        physics=PhysicsGame()      
        physics.run(screen, WIDTH, HEIGHT)
    elif stats==True:
        victory_channel.pause()
        stats_channel.unpause()
        main_channel.pause()
        screen.fill((255, 224, 130))
        draw_text(f'x{MS.player.cheezy}', font, WOOD_BROWN, 45, 70)
        draw_text(f'Attack Level:{attack_level}', font, BLACK, 180, 330)
        draw_text(f'Defense Level: {MS.defense_level}', font, BLACK, 450, 130)
        draw_text(f'Health Level:{health_level}', font, BLACK, 730, 350)
        screen.blit(cheezy_img, (10, 65))        
        attack_stats_button.draw(screen)
        defense_stats_button.draw(screen)
        health_stats_button.draw(screen)
        pizza_stats3.draw(screen)
        #pizza_attack_stats_dict = {1: pizza_stats1, 2: pizza_stats2, 3: pizza_stats3}
        #pizza_defense_stats_dict = {1: pizza_stats1, 2: pizza_stats2, 3: pizza_stats3}
        #pizza_health_stats_dict = {1: pizza_stats1, 2: pizza_stats2, 3: pizza_stats3}      
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
        elif stats_add_defense_button.draw(screen):
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
        elif stats_add_health_button.draw(screen):
            if health_level==3:
                maximum_level_visible=True
                start_time = pygame.time.get_ticks()
            else:
                if MS.player.cheezy!=0:
                    MS.player.cheezy-=1
                    health_level+=1
                    player.health+=40
                    
                    print(f"health_level:{health_level}")
                    print(f"cheezy:{MS.player.cheezy}")
                    print(f"player health:{player.health}")
                else:
                    warning_cheezy_visible=True
                    start_time = pygame.time.get_ticks()
  
 
        if stats_return_button.draw(screen):
            pause_menu=True
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

    elif game_over:
        screen.blit(game_over_background_img,(0,0))
        main_channel.pause()
        game_over_channel.unpause()
        start_game=False
        if game_over_retry_button.draw(screen):
            time.wait(500)
            game_over=False
            restart()
            main_channel.unpause()
            game_over_channel.pause()
    elif start_game:
        game()


    pygame.display.update() 

pygame.quit()