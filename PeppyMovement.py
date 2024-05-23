import pygame
import os
from environment import Environment
import csv

pygame.init()


"""SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)"""
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
SCROLL_THRESH = 200
ROWS = 20
COLS = 200
WIDTH = 1000
HEIGHT = 500
TILE_SIZE = HEIGHT // ROWS
TILE_TYPES = 16
screen_scroll = 0
bg_scroll = 0
level = 1

img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'resources/Interactive Elements/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Peppy the Pizza') # changed name

# set framerate
clock = pygame.time.Clock()
FPS = 60

# define game variables
GRAVITY = 0.75


# define player action variables
moving_left = False
moving_right = False 
shoot = False 

tile_size = 50
tile_size_2 = 40
tile_size_3 = 70

# load image
background_img = pygame.image.load("images/background.jpg")

# load images
# Pepperoni (bullet)
# !!update image
# pepperoni_img = pygame.image.load('img/pepperoni.png').convert_alpha()


# define colours
BG = (252,244,163)
WOOD_BROWN = (193, 154, 107) 


""""def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, WOOD_BROWN,(0,300), (SCREEN_WIDTH, 300) )# start and end coordinate"""

# create as sprite class
class Character(pygame.sprite.Sprite):
    # methods
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True 
        self.char_type = char_type
        self.speed = speed 
        self.direction = 1
        self.flip = False
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        
        # load all images for the players
        animation_types = ['Idle', 'Roll', 'Jump']
        for animation in animation_types:
            # reset temporary list of images
            temp_list = []
            # count number of files in the folder
            num_of_frames = len(os.listdir(f"images/{self.char_type}/{self.char_type}_{animation}_Frames"))
            for i in range(num_of_frames):
                img = pygame.image.load(f"images/{self.char_type}/{self.char_type}_{animation}_Frames/{self.char_type}_{animation}_Frame{i}.png").convert_alpha() # add file directory of the pic
                img = pygame.transform.scale(img, (int(img.get_width()*scale), int(img.get_height()*scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)    
        
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update_animation(self):
        # update animation
        ANIMATION_COOLDOWN = 100 # millisecond # used as timer, = speed of animation
        # update imgae depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update (compare current time with last update time)
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks() # reset timer
            self.frame_index += 1

        # if the animation has run out then reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0 

    def update_action(self, new_action):
        # check if the new action is different from the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()



    def move(self, moving_left, moving_right):
        # reset movement variables
        screen_scroll = 0
        dx = 0 # will need these for collision
        dy = 0

        # assign movement variables if moving left or right
        if moving_left == True:
            dx = -self.speed 
            self.flip = True
            self.direction = -1
        if moving_right == True:
            dx = self.speed 
            self.flip = False
            self.direction = 1

        # jump 
        if self.jump == True and self.in_air == False:
            self.vel_y =-17
            self.jump = False
            self.in_air = True 
        
        # apply gravity
        self.vel_y += GRAVITY # +gravity pulling down 
        if self.vel_y > 10:
            self.vel_y = 10 # set limit not more than 10 
        dy += self.vel_y

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

        environment = Environment(img_list)
        environment.process_data(environment_data)

        collision_list = environment.collision_list

        # check for collision 
        for tile in collision_list:
            # check collision in the x direction between rect
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            # check collision in the y direction between rect
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # check if below the ground, jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top # head
                # check if above the ground, falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom # feet 

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        # update scroll based on player position
        if self.char_type == 'player':
            if self.rect.right > SCREEN_WIDTH - SCROLL_THRESH:
                self.rect.x -= dx
                screen_scroll = -dx
            elif self.rect.left < SCROLL_THRESH:
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll
    

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect) # put character image into the rectangle

class Pepperoni(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        # define instances
        self.speed = 10 # every bullet have the same speed
        # self.image = pepperoni_img
        self.image = pygame.Surface((12,12))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction

    def update(self):
        # move pepperoni
        self.rect.x += (self.direction * self.speed)
        # check if pepperoni has gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH: # right hand side of bullet to the left of screen, vice versa
            self.kill()

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
