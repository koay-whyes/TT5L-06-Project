import pygame
from pygame.locals import *

SCREEN_SIZE = (1000,500)

pygame.init()

# creates window
pygame.display.set_caption("Peppy the Pizza")
screen = pygame.display.set_mode(SCREEN_SIZE)

tile_size = 50
tile_size_2 = 40
tile_size_3 = 70

# load image
background_img = pygame.image.load("random/background.jpg")

class Environment():
    def __init__(self, data):
        self.tile_list = []
        # load image
        block_img = pygame.image.load('random/block.png')
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

environment_data =[
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0],
[0,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0],
[0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[1,1,1,1,1,0,1,1,1,0,0,1,1,1,1,1,1,1,1,1],
]

environment = Environment(environment_data)

# creates game loop
run = True
while run:
    screen.blit(background_img, (0,0))

    environment.draw()

    # gets user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
      