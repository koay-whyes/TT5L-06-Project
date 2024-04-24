import pygame
import sys

SCREEN_SIZE = (960,540)
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
            pygame.Rect(0,440,960,100),
            pygame.Rect(100,300,200,50),
            pygame.Rect(300,150,500,70)
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
            self.clock.tick(30)

Environment().run()
      