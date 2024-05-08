import pygame
import os

pygame.init()


"""SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)"""
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500

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

        # check collision with floor
        if self.rect.bottom + dy > SCREEN_HEIGHT - tile_size:
            dy = SCREEN_HEIGHT - (tile_size + self.rect.bottom)
            self.in_air = False 

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy
    

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

class Environment():
    def __init__(self, data):
        self.tile_list = []
        # load image
        block_img = pygame.image.load('images/block.png')
        # cuttingboard_image = pygame.image.load('')

        row_count = 0
        for row in data:
            col_count = 0  
            for block in row:
                if block == 1:
                    img = pygame.transform.scale(block_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if block == 2:
                    img = pygame.transform.scale(block_img, (tile_size_2, tile_size_2))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size_2
                    img_rect.y = row_count * tile_size_2
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
