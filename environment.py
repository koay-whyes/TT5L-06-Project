import pygame
import sys

SCREEN_SIZE = (700,500)
BANANA = (252,244,163)
WOOD_BROWN = (193, 154, 107)

class Environment:
    def __init__(self):
        pygame.init()

        # creates window, sets resolution
        pygame.display.set_caption("Peppy the Pizza")
        self.screen = pygame.display.set_mode(SCREEN_SIZE)

        # frame rate
        self.clock = pygame.time.Clock()

    def Platform(self):
        self.platforms = [
            pygame.Rect(0,400,700,100),
            pygame.Rect(50,250,200,50),
            pygame.Rect(200,100,400,50)
        ]
        for self.platform in self.platforms:
            pygame.draw.rect(self.screen, WOOD_BROWN, self.platform)

    def draw_environment(self):
        self.screen.fill(BANANA)
        self.Platform()
        pygame.display.update()
      

    def run(self):
        # creates game loop
        while True:
            # gets user input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.draw_environment()
            # fps
            self.clock.tick(60)

Environment().run()