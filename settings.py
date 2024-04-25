# game options/settings
TITLE = "Peppy the Pizza"
WIDTH = 960
HEIGHT = 540
FPS = 60  # how fast the game runs

# Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12 # how quick to stop, max speed , small num -> faster, takes longer to stop
PLAYER_GRAV = 0.8 # downwards-gravity

# Starting platforms
PLATFORM_LIST = [(0, HEIGHT - 40, WIDTH, 40),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20),
                 (125, HEIGHT - 350, 100,20),
                 (350, 200, 100, 20),
                 (175, 100, 50, 20),
                 (0,440,960,100),
                 (100,300,200,50),
                 (300,150,500,70)]

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)
BANANA = (252,244,163)
WOOD_BROWN = (193, 154, 107)
