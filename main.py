import pygame as pg # rename pygame as pg, to save time retyping "pygame"
import random
# import settings (but to refer to variable, need to type filename.variable, eg: settings.WIDTH)
from  settings import * # later no need "filename.variable"
from sprites import *

class Game: # what this object do
    def __init__(self): # things happen when the game starts 
        # initialize game window, etc
        pg.init() # initialize pygame
        pg.mixer.init() # sound
        self.screen = pg.display.set_mode((WIDTH, HEIGHT)) # class variable needs self.variable
        pg.display.set_caption(TITLE) # display on top of the window
        self.clock = pg.time.Clock() # speed
        # pass # = do nothing (temporary placeholder)
        self.running = True # initialize

    def new(self):
        # Reset/start a new game (not initialize the whole program, just the game)
        self.all_sprites = pg.sprite.Group() # put every sprite into this group
        self.platforms = pg.sprite.Group()
        self.player = Player(self) # for the player to refer when spawn
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(*plat) # exploding the list = break list into small pieces # can do by (plat[0], plat[1], plat[2], plat[3])
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    def run(self): 
        # Game Loop
        self.playing = True 
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        
    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False) 
            # false: to not delete anything when collide
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window (at anytime)
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            # if spacebar is pressed, player jump
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BANANA) # can straight away put the colour code here
        self.all_sprites.draw(self.screen)
        # *after* drawing everything, flip the display (time efficiency). CANNOT flip -> display
        pg.display.flip() 

    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        pass

g = Game() # new game object
g.show_start_screen() # start screen
while g.running:
    g.new() # start game
    # g.run() # OR run in the new(self) function
    g.show_go_screen() # game over screen #??? should be excluded from running or not?

pg.quit()
