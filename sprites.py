# Sprites classes for platform game
import pygame as pg 
from settings import *
vec = pg.math.Vector2 # 2 dimensional vector, to control accln, speed easier

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game 
        self.image = pg.Surface((30,40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2) # start at center position
        self.vel = vec(0,0) # (x,y)
        self.acc = vec(0,0) # acceleration
        
    def jump(self):
        # jump only if standing on a platform
        self.rect.x += 1 # 1 pixel lower(?)
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1 # move 1 pixel up # purpose: shift down temporarily to see if there's anything below(??)
        if hits:
            self.vel.y = -20

    def update(self):
        # self.vx = 0 # if don't set this, rect will constantly go right/left
        self.acc = vec(0, PLAYER_GRAV) # keypress control accln 
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION # higher speed, more friction + having a max speed
        # equations of motion
        self.vel += self.acc 
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0 # self.pos.x = WIDTH makes the rect cannot escape
        if self.pos.x < 0:
            self.pos.x = WIDTH
        self.rect.midbottom = self.pos # use midbottom instead of center to easily locate sprite on top of the platform

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h): # x,y where to locate sprite when respawn, # w, h for size of platform
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
