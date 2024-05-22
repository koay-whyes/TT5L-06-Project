import pygame
from pygame.locals import *
import csv
import PeppyMovement as PM

WIDTH = 1000
HEIGHT = 500
ROWS = 20
COLS = 200
TILE_SIZE = HEIGHT // ROWS

class Environment():
    def __init__(self, img_list):
        # tiles with collision
        self.collision_list = []
        self.img_list = img_list

    # data is from csvfile
    def process_data(self, data):
        # iterate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                # -1 ignored
                if tile >= 0:
                    # get image
                    img = self.img_list[tile]
                    # get rectangle
                    img_rect = img.get_rect()
                    # get position
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    # tiles with collision
                    if tile >= 0 and tile <= 13:
                        self.collision_list.append(tile_data)
                    # environmental threats
                    # elif tile >= 14:
                    #     pass
                    # checkpoint
                    elif tile == 14 and tile == 15:
                        pass

    def draw(self, surface):
        for tile in self.collision_list:
            tile[1][0] += PM.screen_scroll
            # img and rect
            surface.blit(tile[0], tile[1])