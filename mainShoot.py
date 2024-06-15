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
TILE_TYPES = 39
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
dash_board_img = loadify('img/Interactive Elements/tiles/36.png')
dash_board_img = pygame.transform.scale(dash_board_img, (200, 200))
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
cheezy_board_img = loadify('img/Interactive Elements/tiles/38.png') 
cheezy_board_img = pygame.transform.scale(cheezy_board_img, (100, 100))

item_boxes = {
    'Health'	: health_box_img,
    'Ammo'		: ammo_box_img,
    'Cheezy'    : cheezy_img
}
decorative_items = {
    'Cutting Board' : cutting_board_img,
    'Mug' : mug_img,
    'Pan' : pan_img,
    'Towel' : towel_img,
    'Dash Board' : dash_board_img,
    'Cheezy Board' : cheezy_board_img
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
                    elif tile == 38:
                          decoration = Decoration("Cheezy Board", x * TILE_SIZE, y * TILE_SIZE)
                          decoration_group.add(decoration)
                    elif tile == 36:
                          decoration = Decoration("Dash Board", x * TILE_SIZE, y * TILE_SIZE)
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
                    elif tile == 34: # level 1 enemy
                        enemy = Character('Broccoli', x * TILE_SIZE, y * TILE_SIZE, 1.65, 2, 3)
                        enemy_group.add(enemy)
                    elif tile == 35: # level 2 enemy
                        enemy = Character('Anchovy', x * TILE_SIZE, y * TILE_SIZE, 1.65, 2, 7)
                        enemy_group.add(enemy)                        
                    elif tile == 26: # level 3 enemy
                        enemy = Character('Pineapple', x * TILE_SIZE, y * TILE_SIZE, 1.65, 2, 10)
                        enemy_group.add(enemy)
                    elif tile == 37: # final boss
                        enemy = Character('Boss', x * TILE_SIZE, y * TILE_SIZE, 1.65*1.2, 2, 20)
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




            # Clear the screen
            screen.fill(WHITE)

            # Draw the Pymunk shapes
            self.space.debug_draw(draw_options)
            image_x = self.body_body.position.x - self.body_image.get_width() / 2
            image_y = self.body_body.position.y - self.body_image.get_height() / 2
            screen.blit(self.body_image, (image_x, image_y))


            text1 = font.render("CREDITS", True, 'black')

            text2 = font.render("Developed by students from group TT5L-06:  ", True, 'black')
            text3 = font.render("Chew Jia Yi, Koay Yee Shuen, Ong Wan Ning", True, 'black')
            text4 = font.render("For Mini IT Project, Foundation in IT, MMU", True, 'black')

            text5 = font.render("Try to move Peppy around!", False, 'black')
            
            screen.blit(text1, (630, 40))
            screen.blit(text2, (450, 70))
            screen.blit(text3, (450, 100))
            screen.blit(text4, (450, 130))
            screen.blit(text5, (40, 380))


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

