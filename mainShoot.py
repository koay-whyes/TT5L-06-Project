import pygame
import os
import random
import csv
import time
import pymunk
import pymunk.pygame_util

pygame.init()


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.5)

flags = pygame.HWSURFACE | pygame.DOUBLEBUF
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
pygame.display.set_caption('Peppy the Pizza')

# set framerate
clock = pygame.time.Clock()
FPS = 60

# define game variables
GRAVITY = 0.75
SCROLL_THRESH = 400
ROWS = 20
COLS = 640
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 36
MAX_LEVELS = 3
screen_scroll = 0
bg_scroll = 0
level = 1
defense_level=0
level_complete=False

# define player action variables
moving_left = False
moving_right = False 
shoot = False 

#sound
shoot_fx = pygame.mixer.Sound("sound/shoot.mp3")
cheezy_fx = pygame.mixer.Sound("sound/cheezy.mp3")
item_fx = pygame.mixer.Sound("sound/item.mp3")
pizzabox_fx = pygame.mixer.Sound("sound/pizzabox.mp3")
fall_fx = pygame.mixer.Sound("sound/fall.mp3")

def loadify(imgname):
    return pygame.image.load(imgname).convert_alpha()

# load images
# store tiles in a list
img_list = []
for x in range(TILE_TYPES):
    img = loadify(f'img/Interactive Elements/tiles/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)
# Pepperoni (bullet)




pepperoni_img = loadify('img/icons/pepperoni.png') 
#pick up boxes
health_box_img = loadify('img/Interactive Elements/tiles/28.png') 
ammo_box_img = loadify('img/Interactive Elements/tiles/27.png') 
cheezy_img = loadify('img/Interactive Elements/tiles/21.png') 
cheezy_frames = [loadify(f'img/Interactive Elements/Cheezys/{i}.png') for i in range(21,26)]
cutting_board_img = loadify('img/Interactive Elements/tiles/29.png') 
cutting_board_img = pygame.transform.scale(cutting_board_img, (200, 200))
mug_img = loadify('img/Interactive Elements/tiles/30.png') 
mug_img = pygame.transform.scale(mug_img, (95, 95))
pan_img = loadify('img/Interactive Elements/tiles/31.png') 
pan_img = pygame.transform.scale(pan_img, (100, 100))
towel_img = loadify('img/Interactive Elements/tiles/32.png') 
towel_img = pygame.transform.scale(towel_img, (125, 125))
sink_img = loadify('img/Interactive Elements/tiles/22.png') 
sink_img = pygame.transform.scale(sink_img, (70, 70))
oil_img = loadify('img/Interactive Elements/tiles/23.png') 
sink_tile_img = loadify('img/Interactive Elements/tiles/33.png') 
sink_tile_img = pygame.transform.scale(sink_tile_img, (TILE_SIZE, TILE_SIZE))
oil_tile_img = loadify('img/Interactive Elements/tiles/24.png') 

item_boxes = {
    'Health'	: health_box_img,
    'Ammo'		: ammo_box_img,
    'Cheezy'    : cheezy_img
}
decorative_items = {
    'Cutting Board' : cutting_board_img,
    'Mug' : mug_img,
    'Pan' : pan_img,
    'Towel' : towel_img
}
threat_items = {
    'Sink' : sink_img,
    'Oil' : oil_img,
    'Sink Tile' : sink_tile_img,
    'Oil Tile' : oil_tile_img
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

"""def draw_bg():
    screen.fill(BG)"""
    

# fixed the bullet-character gap problem
def custom_collision(character, pepperoni_group):
    # Calculate the centers
    pepperoni_center = pepperoni_group.rect.center
    character_center = character.rect.center
        
    # Define a distance threshold, e.g., 10 pixels towards the center
    distance_threshold = 10
        
    # Check if the bullet is within the threshold distance to the character's center
    return pygame.math.Vector2(pepperoni_center).distance_to(character_center) <= distance_threshold

# create as sprite class
class Character(pygame.sprite.Sprite):
    # methods
    def __init__(self, char_type, x, y, scale, speed, ammo):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True 
        self.char_type = char_type
        self.speed = speed 
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.cheezy = 0
        self.health = 120 # self.health = health for diff health for peppy and enemy
        self.max_health = self.health # for health bar
        self.direction = 1
        self.flip = False
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        #ai specific variables
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.idling = False
        self.idling_counter = 0
        # dash
        self.dash_duration = 0.3  # Dash duration in seconds
        self.dash_cooldown = 1  # Cooldown between dashes in seconds
        self.last_dash = 0
        self.dash_start_time = 0
        self.base_speed = self.speed 
        
        # load all images for the players
        animation_types = ['Idle', 'Roll', 'Jump', 'Dead', 'Attack']
        for animation in animation_types:
            # reset temporary list of images
            temp_list = []
            # count number of files in the folder
            num_of_frames = len(os.listdir(f"img/{self.char_type}/{self.char_type}_{animation}_Frames"))
            for i in range(num_of_frames):
                img = loadify(f"img/{self.char_type}/{self.char_type}_{animation}_Frames/{self.char_type}_{animation}_Frame{i}.png")  # add file directory of the pic
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
            if self.action == 3 or self.action == 4:
                self.frame_index = len(self.animation_list[self.action]) -1
            else:
                self.frame_index = 0 

        

    def update_action(self, new_action):
        # check if the new action is different from the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def update(self):
        self.update_animation()
        self.check_alive()
        # update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right, dash):
        # reset movement variables
        global bg_scroll
        global screen_scroll
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
        
        # Dash logic
        """if dash and time.time() - self.last_dash > self.dash_cooldown:
            if moving_left:
                dx -= self.dash_distance
                self.last_dash = time.time()
                dash = True
            if moving_right:
                dx += self.dash_distance"""
        
        if dash and time.time() - self.last_dash > self.dash_cooldown:
            self.dash_start_time = time.time()
            self.speed = self.base_speed * 5
            
            """if moving_left:
                dx -= self.speed
            if moving_right:
                dx += self.speed"""
            
            self.last_dash = time.time()
        
        if time.time() - self.dash_start_time > self.dash_duration:
            self.dash = False 
            self.speed = self.base_speed
            
        # jump 
        if self.jump == True and self.in_air == False:
            self.vel_y =-20
            self.jump = False
            self.in_air = True 
        
        # apply gravity
        self.vel_y += GRAVITY # +gravity pulling down 
        if self.vel_y > 10:
            self.vel_y = 10 # set limit not more than 10 
        dy += self.vel_y

        """# check collision with floor
        if self.rect.bottom + dy >300:
            dy = 300 - self.rect.bottom
            self.in_air = False """
        #check for collision
        for tile in world.obstacle_list:
            #check collision in the x direction
            if isinstance(tile, MovingPlatform):
                if tile.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                if tile.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        self.vel_y = 0
                        dy = tile.rect.bottom - self.rect.top
                    # above moving platforms
                    elif self.vel_y >= 0:
                        self.vel_y = 0
                        self.in_air = False
                        dy = tile.rect.top - self.rect.bottom   
                        self.rect.x += tile.move_direction 
            else:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                    # if the ai hit obstacles, make them turn around
                    if self.char_type == "enemy":
                        self.direction *= -1
                        self.move_counter = 0                 
                #check for collision in the y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #check if below the ground, i.e. jumping
                    if self.vel_y < 0:
                        self.vel_y = 0
                        dy = tile[1].bottom - self.rect.top
                    #check if above the ground, i.e. falling
                    elif self.vel_y >= 0:
                        self.vel_y = 0
                        self.in_air = False
                        dy = tile[1].top - self.rect.bottom        
        
        # check for collision with threats
        if pygame.sprite.spritecollide(self, threat_group, False):
            self.health = 0

        # check if player fallen off the map 
        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0

        # check for collision with pizza box (exit)
        global level_complete
        if pygame.sprite.spritecollide(self, exit_group, False):
            level_complete = True
            pizzabox_fx.play()
        
        # check if going off the edge of the screen
        if self.char_type == 'Peppy':
            if self.rect.x + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0
            """if self.rect.y + dy > SCREEN_HEIGHT:
                self.alive = False """

        # update rectangle position
        self.rect.x += dx 
        self.rect.y += dy

        # update scroll based on player position
        screen_scroll = 0
        if self.char_type == 'Peppy':
            max_scroll = (world.level_length * TILE_SIZE) - SCREEN_WIDTH
            # Check if player is near the screen edges and needs to scroll
            if self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and dx > 0 and bg_scroll < max_scroll:
                self.rect.x -= dx
                screen_scroll = -dx
                bg_scroll -= screen_scroll
            elif self.rect.left < SCROLL_THRESH and dx < 0 and bg_scroll > abs(dx):
                self.rect.x -= dx
                screen_scroll = -dx
                bg_scroll -= screen_scroll
            else:
                self.rect.x += dx

        return screen_scroll, level_complete
    
    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20 # reload speed of bullet
            pepperoni = Pepperoni(self.rect.centerx + (0.5 * self.rect.size[0]*self.direction), self.rect.centery, self.direction)
            pepperoni_group.add(pepperoni)
            # reduce ammo
            self.ammo -= 1
            shoot_fx.play()
    
    def ai(self, screen_scroll):
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0)#0: idle
                self.idling = True
                self.idling_counter = 50
            #check if the ai in near the player
            if self.vision.colliderect(player.rect):
                #stop running and face the player
                self.update_action(0)#0: idle
                #shoot
                self.shoot()
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right, False)
                    self.update_action(1)#1: run
                    self.move_counter += 1
                    #update ai vision as the enemy moves
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False
        # scrolling
        self.rect.x += screen_scroll
    
    def check_alive(self):
        if self.health <= 0 :
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3) #dead animation

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect) # put character image into the rectangle

class MovingPlatform(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.start_x = x
        self.start_y = y
        self.move_counter = 0
        self.move_direction = 1


    def update(self):
        # moving the platforms
        self.rect.x = self.start_x + self.move_counter * self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50 :
            self.move_direction *= -1
            self.move_counter *= 0
    






class World():
    def __init__(self):
        self.obstacle_list = []
        self.level_length = 0

    # world data list
    def process_data(self, data, level):
        self.level_length = len(data[0]) # columns
        #iterate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    # platforms
                    if tile >= 0 and tile <= 17:
                        self.obstacle_list.append(tile_data)
                    # moving platforms
                    elif tile == 18:
                        moving_platform = MovingPlatform(img, x * TILE_SIZE, y * TILE_SIZE)
                        self.obstacle_list.append(moving_platform)
                        moving_platform_group.add(moving_platform)
                    elif tile == 22:
                         threat = Threat('Sink', x * TILE_SIZE, y * TILE_SIZE)
                         threat_group.add(threat)
                    elif tile == 23:
                         threat = Threat('Oil', x * TILE_SIZE, y * TILE_SIZE)
                         threat_group.add(threat)
                    elif tile == 24:
                         threat = Threat('Oil Tile', x * TILE_SIZE, y * TILE_SIZE)
                         threat_group.add(threat)
                    elif tile == 33:
                         threat = Threat("Sink Tile", x * TILE_SIZE, y * TILE_SIZE)
                         threat_group.add(threat)
                    elif tile == 29:
                          decoration = Decoration("Cutting Board", x * TILE_SIZE, y * TILE_SIZE)
                          decoration_group.add(decoration)
                    elif tile == 30:
                          decoration = Decoration("Mug", x * TILE_SIZE, y * TILE_SIZE)
                          decoration_group.add(decoration)
                    elif tile == 31:
                          decoration = Decoration("Pan", x * TILE_SIZE, y * TILE_SIZE)
                          decoration_group.add(decoration)
                    elif tile == 32:
                          decoration = Decoration("Towel", x * TILE_SIZE, y * TILE_SIZE)
                          decoration_group.add(decoration)
                    elif tile == 25:#create player
                        player = Character('Peppy', x * TILE_SIZE, y * TILE_SIZE, 1.65, 5, 20)
                        health_bar = HealthBar(10, 10, player.health, player.health)
                    elif tile == 26:#create enemies
                        if level == 1:
                            enemy = Character('Pineapple', x * TILE_SIZE, y * TILE_SIZE, 1.65, 2, 20)
                            enemy_group.add(enemy)
                        elif level == 2:
                            enemy = Character('Anchovy', x * TILE_SIZE, y * TILE_SIZE, 1.65, 2, 20)
                            enemy_group.add(enemy)
                    elif tile == 27:#create ammo box
                         item_box = ItemBox('Ammo', x * TILE_SIZE, y * TILE_SIZE)
                         item_box_group.add(item_box)
                    elif tile == 28:#create health box
                         item_box = ItemBox('Health', x * TILE_SIZE, y * TILE_SIZE)
                         item_box_group.add(item_box)
                    elif tile == 21:#create cheezy
                          cheezy = ItemBox('Cheezy', x * TILE_SIZE, y * TILE_SIZE)
                          decoration_group.add(cheezy)
                    elif tile == 19:#create exit (pizza box)
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)

        return player, health_bar


    def draw(self):
        for tile in self.obstacle_list:
            if isinstance(tile, MovingPlatform):
                  tile.start_x += screen_scroll
                  tile.update()
                  screen.blit(tile.image, tile.rect)
            else:
                  tile[1][0] += screen_scroll
                  screen.blit(tile[0], tile[1])


class Decoration(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = decorative_items[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self, screen_scroll):
        self.rect.x += screen_scroll



class Threat(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = threat_items[self.item_type]
        # self.image = pygame.transform.scale(img, (75, 75))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self, screen_scroll):
        self.rect.x += screen_scroll

class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(img, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self, screen_scroll):
        self.rect.x += screen_scroll


class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        if self.item_type == "Cheezy":
            self.frames =  cheezy_frames
            self.current_frame = 0
            self.last_update = pygame.time.get_ticks()
            self.frame_rate = 100
            self.image = self.frames[self.current_frame]
        else:
            self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self, screen_scroll):
        self.rect.x += screen_scroll

        if self.item_type == "Cheezy":
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.frames[self.current_frame]

        #check if the player has picked up the box
        if pygame.sprite.collide_rect(self, player):
            #check what kind of box it was
            if self.item_type == 'Health':
                player.health += 25
                item_fx.play()
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == 'Ammo':
                player.ammo += 15
                item_fx.play()
            elif self.item_type == 'Cheezy':
                player.cheezy += 1
                cheezy_fx.play()
            print(player.cheezy)
            #delete the item box
            self.kill()

class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health):
        #update with new health
        self.health = health
        #calculate health ratio
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))

class Pepperoni(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        # define instances
        self.speed = 10 # every bullet have the same speed
        self.image = pepperoni_img
        # self.image = pygame.Surface((12,12))
        # self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction


    
    def update(self):
        # move pepperoni
        self.rect.x += (self.direction * self.speed) + screen_scroll
        # check if pepperoni has gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH: # right hand side of bullet to the left of screen, vice versa
            self.kill()

        #check for collision with level
        for tile in world.obstacle_list:
            if isinstance(tile, MovingPlatform):
                if tile.rect.colliderect(self.rect):
                    self.kill()
            elif tile[1].colliderect(self.rect):
                self.kill()
                    
        # check collision with characters
        if pygame.sprite.spritecollide(player, pepperoni_group, False, custom_collision):
            if player.alive:
                damage_amounts = {0: 10, 1: 8, 2: 6, 3: 4}
                player.health -= damage_amounts.get(defense_level, 10)
                self.kill()  # delete bullet
       
        
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, pepperoni_group, False, custom_collision):
                if enemy.alive:
                    
                    enemy.health -= 20
                    self.kill() # delete bullet 

class PhysicsGame():
    def __init__(self, width=1000, height=500):
        self.width = width
        self.height = height
        self.screen = None
        self.space = None
        self.dt = 1 / 60
        self.last_jump_time = 0
        self.jump_cooldown = 2

        self.body_body = None
        self.body_shape = None
        self.body_image = None

        #story
        self.story_texts = [ 

            "Long ago, all the pizza ingredients lived together in harmony.(PRESS ENTER)",
            "Then, everything changed when the Pineapple attacked.(PRESS ENTER)",
            "Only the pepperoni pizza, Peppy, with its superpizza abilities could stop him.(PRESS ENTER)",
            "He will need the help of the power ups and the cheezys to stand a chance to defeat the Pineapple.",
            "And of course, yours!(PRESS NEXT TO START THE GAME)",
        ]

        self.story_index = 0
        self.enter_key_down = False

    def create_boundaries(self, space, width, height):
        rects = [
            [(width/2, height - 10/10), (width, 20/10)],
            [(width/2, 10/10), (width, 20/10)],
            [(10/10, height/2), (20/10, height)],
            [(width - 10/10, height/2), (20/10, height)]
        ]

        for pos, size in rects:
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            body.position = pos
            shape = pymunk.Poly.create_box(body, size)
            shape.mass = 100000
            shape.elasticity = 0.4
            shape.friction = 0.8
            space.add(body, shape)

    def create_structure(self, space, width, height):
        BROWN = (139, 69, 19, 100)
        rects = [
            [(600, height - 120), (40, 200), BROWN, 100],
            [(900, height - 120), (40, 200), BROWN, 100],
            [(750, height - 240), (340, 40), BROWN, 150]
        ]

        for pos, size, color, mass in rects:
            body = pymunk.Body()
            body.position = pos
            shape = pymunk.Poly.create_box(body, size, radius=2)
            shape.color = color
            shape.mass = mass
            shape.elasticity = 0.4
            shape.friction = 0.4
            space.add(body, shape)

    def create_swinging_ball(self, space):
        rotation_center_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        rotation_center_body.position = (300, 100)

        body = pymunk.Body()
        body.position = (300, 150)
        line = pymunk.Segment(body, (0, 0), (200, 0), 5)
        circle = pymunk.Circle(body, 40, (200, 0))
        line.friction = 1
        circle.friction = 1
        line.mass = 8
        circle.mass = 30
        circle.elasticity = 0.95
        circle.color = (128, 128, 128,0)
        line.color = (128, 128, 128,0)
        rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0, 0), (0, 0))
        space.add(circle, line, body, rotation_center_joint)

    def run(self, screen, width, height):

        run = True

        self.space = pymunk.Space()
        self.space.gravity = (0, 981)
        self.last_jump_time = 0
        self.jump_cooldown = 2  # 2 seconds

        # Create the body
        self.body_body = pymunk.Body(1, 1666)
        self.body_body.position = (100, 100)

        # Create the shape for the body
        self.body_shape = pymunk.Circle(self.body_body, 50)
        self.body_shape.elasticity = 0.2
        self.body_shape.friction = 0.1
        self.body_shape.color = (255, 255, 255, 0)
        self.body_image = pygame.image.load("img/Peppy/Peppy_Fall_Frames/Peppy_Fall_Frame1.png")
        self.body_image = pygame.transform.scale(self.body_image, (100, 100))

        # Add the body and shape to the space
        self.space.add(self.body_body, self.body_shape)

        self.create_boundaries(self.space, width, height)
        self.create_structure(self.space, width, height)
        self.create_swinging_ball(self.space)

        draw_options = pymunk.pygame_util.DrawOptions(screen)

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.enter_key_down = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RETURN:
                        self.enter_key_down = False

            keys = pygame.key.get_pressed()

            # Move the body left and right
            if keys[pygame.K_a]:
                self.body_body.velocity = (-200, self.body_body.velocity.y)
            if keys[pygame.K_d]:
                self.body_body.velocity = (200, self.body_body.velocity.y)

            # Jump
            current_time = pygame.time.get_ticks() / 1000
            if keys[pygame.K_w] and abs(self.body_body.velocity.y) < 1 and current_time - self.last_jump_time > self.jump_cooldown:
                self.body_body.apply_impulse_at_local_point((0, 1000), (0, 0))
                self.last_jump_time = current_time

            if self.enter_key_down:
                self.story_index = (self.story_index + 1) % len(self.story_texts)


            # Clear the screen
            screen.fill(WHITE)

            # Draw the Pymunk shapes
            self.space.debug_draw(draw_options)
            image_x = self.body_body.position.x - self.body_image.get_width() / 2
            image_y = self.body_body.position.y - self.body_image.get_height() / 2
            screen.blit(self.body_image, (image_x, image_y))

            # NPC dialogue
            text = font.render(self.story_texts[self.story_index], True, BLACK)
            screen.blit(text, (40, 400))


            # Flip the screen
            pygame.display.flip()

            self.space.step(self.dt)
            clock.tick(FPS)

        pygame.quit()

# create sprite groups
enemy_group = pygame.sprite.Group()
pepperoni_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
threat_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
moving_platform_group =  pygame.sprite.Group()






# create an player instance of the class for player
"""player = Character("Peppy",200,200,1.65, 5, 20)
health_bar = HealthBar(10, 10, player.health, player.health)
enemy = Character("Pineapple",500, 200, 1.65, 2, 20) # change char type later
enemy2 = Character('Pineapple', 300, 200, 1.65, 2, 20)		
enemy_group.add(enemy)		
enemy_group.add(enemy2)"""

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

