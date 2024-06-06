import pygame
import menubutton
import csv

pygame.init()

clock = pygame.time.Clock()
fps = 60

# game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
LOWER_MARGIN = 200
SIDE_MARGIN = 400

# level editor screen
screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption("Level Editor")

# game variables
ROWS = 20
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 36
current_tile = 0
level = 0
COLS = 200
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1

# load images
background_images = {
    1: pygame.image.load("img/level_1.png").convert_alpha(),
    2: pygame.image.load("img/level_2.png").convert_alpha(),
    3: pygame.image.load("img/level_1.png").convert_alpha()
}
# store images in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'img/Interactive Elements/tiles/{x}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

save_img = pygame.image.load('img/button_1.png').convert_alpha()
load_img = pygame.image.load('img/button_2.png').convert_alpha()



# define colours
YELLOW = (255, 250, 205)
WHITE = (255, 255, 255)
RED = (255, 0 , 0)
BLUE = (167, 199, 231)
BLACK = (0, 0, 0)

# define font
font = pygame.font.SysFont("Futura", 30)



# create empty tile list
environment_data = []
# create environment data list
for row in range(ROWS):
    row = [-1] * COLS
    environment_data.append(row)

# create base platform
for tile in range(0, COLS):
    environment_data[ROWS - 1][tile] = 0

# putting text onto screen
def draw_text(text, font, text_col, x, y):
    # convert text data to image
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

# drawing background
def draw_background():
    screen.fill(YELLOW)
    background_img = background_images.get(level % len(background_images), background_images[1])
    width = background_img.get_width()
    # loop background image
    for x in range(5):
        # background needs to move left while scrolling right and vice versa
        # a value times with scroll to change scrolling speed
        screen.blit(background_img, ((x * width) -scroll, 0))

# drawing grid
def draw_grid():
    # vertical lines, columns
    # - scroll to take scrolling into account
    for col in range(COLS + 1):
        pygame.draw.line(screen, WHITE, (col * TILE_SIZE - scroll, 0), (col * TILE_SIZE - scroll, SCREEN_HEIGHT))
    # horizontal lines, rows
    for row in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, row * TILE_SIZE), (SCREEN_WIDTH, row * TILE_SIZE))

# drawing tiles
def draw_environment():
    # iterate through environment data list
    # keep count of the row number
    for y, row in enumerate(environment_data):
        # iterate through rows for individual tiles
        for x, tile in enumerate(row):
            # ignore -1
            if tile >= 0:
                screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))

# create buttons
save_button = menubutton.DrawMenu(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 50, save_img, 1)
load_button = menubutton.DrawMenu(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 50, load_img, 1)

# create button list
# tiles in the margin
button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
    # from menubutton file
    tile_button = menubutton.DrawMenu(SCREEN_WIDTH + (75 * button_col) + 25, (75 * button_row) + 50, img_list[i], 1)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 5:
        button_row += 1
        button_col = 0

# loop
run = True
while run:
    clock.tick(fps)

    draw_background()
    draw_grid()
    draw_environment()
    draw_text(f"Level: {level}", font, BLACK, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
    draw_text("Press up or down to change level", font, BLACK, 10, SCREEN_HEIGHT + LOWER_MARGIN - 60)

    # save and load buttons
    if save_button.draw(screen):
        # save level data
        with open(f'level{level}_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter = ",")
            for row in environment_data:
                writer.writerow(row)

    if load_button.draw(screen):
        # load in level data
        # reset scroll
        scroll = 0
        with open(f'level{level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter = ",")
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    environment_data[x][y] = int(tile)


    # draw tile panel and tiles
    pygame.draw.rect(screen, YELLOW, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

    # choose tiles
    button_count = 0
    # iterate through button list
    # enumarate to keep count
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count

    # indicate selected tile
    pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

    # scroll the map, make sure it doesn't scroll past 0
    if scroll_left == True and scroll > 0:
        scroll -= 5 * scroll_speed
    # make sure it doesn't scroll past actual screen
    if scroll_right == True and scroll < (COLS * TILE_SIZE) - SCREEN_WIDTH:
        scroll += 5 * scroll_speed

    # add tiles to the screen
    # get mouse position (x,y)
    pos = pygame.mouse.get_pos()
    # grid postions
    x = (pos[0] + scroll) // TILE_SIZE
    y = pos[1] // TILE_SIZE

    # check that the coordinates are within tile area (not on margins)
    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
        # tile value from mouse clicks
        # left click to change tile
        if pygame.mouse.get_pressed()[0] == 1:
            # update tile
            if environment_data[y][x] != current_tile:
                environment_data[y][x] = current_tile
        # right click to reset tile
        if pygame.mouse.get_pressed()[2] == 1:
            environment_data[y][x] = -1



    # event handler
    for event in pygame.event.get():
        # exit game, presses x
        if event.type == pygame.QUIT:
            run = False
        # keyboard presses
        if event.type == pygame.KEYDOWN:
            # change level number
            if event.key == pygame.K_UP:
                level += 1
            if event.key == pygame.K_DOWN and level > 0:
                level -= 1
            # press left
            if event.key == pygame.K_LEFT:
                scroll_left = True
            # press right
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            # scrolling speed
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 5

        # release key
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 1


    pygame.display.update()

# run only when while loop is completed
pygame.quit()

