import pygame
import os
import random
pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Peppy the Pizza')

# set framerate
clock = pygame.time.Clock()
FPS = 60

# define game variables
GRAVITY = 0.75
TILE_SIZE = 40


# define player action variables
moving_left = False
moving_right = False 
shoot = False 

# load images
# Pepperoni (bullet)
# !!update image
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
    pygame.draw.line(screen, WOOD_BROWN,(0,300), (SCREEN_WIDTH, 300) )# start and end coordinate

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
        self.health = 100 # self.health = health for diff health for peppy and enemy
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
        
        # load all images for the players
        animation_types = ['Idle', 'Roll', 'Jump', 'Dead']
        for animation in animation_types:
            # reset temporary list of images
            temp_list = []
            # count number of files in the folder
            num_of_frames = len(os.listdir(f"img/{self.char_type}/{self.char_type}_{animation}_Frames"))
            for i in range(num_of_frames):
                img = pygame.image.load(f"img/{self.char_type}/{self.char_type}_{animation}_Frames/{self.char_type}_{animation}_Frame{i}.png").convert_alpha() # add file directory of the pic
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
            if self.action == 3:
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
            self.vel_y =-11
            self.jump = False
            self.in_air = True 
        
        # apply gravity
        self.vel_y += GRAVITY # +gravity pulling down 
        if self.vel_y > 10:
            self.vel_y = 10 # set limit not more than 10 
        dy += self.vel_y

        # check collision with floor
        if self.rect.bottom + dy >300:
            dy = 300 - self.rect.bottom
            self.in_air = False 

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy
    
    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20 # reload speed of bullet
            pepperoni = Pepperoni(self.rect.centerx + (0.5 * self.rect.size[0]*self.direction), self.rect.centery, self.direction)
            pepperoni_group.add(pepperoni)
            # reduce ammo
            self.ammo -= 1
	
    def ai(self):
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
                    self.move(ai_moving_left, ai_moving_right)
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
    
    def check_alive(self):
        if self.health <= 0 :
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3) #dead animation

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect) # put character image into the rectangle

class ItemBox(pygame.sprite.Sprite):
	def __init__(self, item_type, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.item_type = item_type
		self.image = item_boxes[self.item_type]
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))


	def update(self):
		#check if the player has picked up the box
		if pygame.sprite.collide_rect(self, player):
			#check what kind of box it was
			if self.item_type == 'Health':
				player.health += 25
				if player.health > player.max_health:
					player.health = player.max_health
			elif self.item_type == 'Ammo':
				player.ammo += 15
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
        self.rect.x += (self.direction * self.speed)
        # check if pepperoni has gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH: # right hand side of bullet to the left of screen, vice versa
            self.kill()

        # check collision with characters
        if pygame.sprite.spritecollide(player, pepperoni_group, False, custom_collision):
            if player.alive:
                player.health -= 5
                self.kill() # delete bullet 

        
        
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, pepperoni_group, False, custom_collision):
                if enemy.alive:
                    
                    enemy.health -= 25
                    self.kill() # delete bullet 






# create sprite groups
enemy_group = pygame.sprite.Group()
pepperoni_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()

#temp - create item boxes
item_box = ItemBox('Health', 100, 260)
item_box_group.add(item_box)
item_box = ItemBox('Ammo', 400, 260)
item_box_group.add(item_box)



# create an player instance of the class for player
player = Character("Peppy",200,200,1.65, 5, 20)
health_bar = HealthBar(10, 10, player.health, player.health)
enemy = Character("Pineapple",500, 200, 1.65, 2, 20) # change char type later
enemy2 = Character('Pineapple', 300, 200, 1.65, 2, 20)		
enemy_group.add(enemy)		
enemy_group.add(enemy2)

run = True
while run:

    clock.tick(FPS)
    
    draw_bg()
    #show player health
    health_bar.draw(player.health)
	#show ammo
    draw_text('AMMO: ', font, WHITE, 10, 35)
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
    item_box_group.update()
    pepperoni_group.draw(screen)
    item_box_group.draw(screen)


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


    # event in pygame: click/press on keyboard
    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            run = False
        # keyboard presses (KEYDOWN)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False 



        # keyboard button released (KEYUP)
        if event.type == pygame.KEYUP: 
            if event.key == pygame.K_a :
                moving_left = False 
            if event.key == pygame.K_d:
                moving_right = False 
            if event.key == pygame.K_SPACE:
                shoot = False 
            

    pygame.display.update()

pygame.quit()