import pygame, menubutton

WIDTH, HEIGHT = 640, 480

screen = pygame.display.set_mode((WIDTH, HEIGHT))
class Scene:
    def on_start(self):
        pass

    def update(self, events):
        pass

    def on_exit(self):
        pass


class Main(Scene):
    def __init__(self, screen, scenes):
        self.scenes  = scenes
        self.screen  = screen
        self.music   = pygame.mixer.Sound("bgm.mp3")
        self.channel = pygame.mixer.Channel(0)

    def on_start(self):
        self.channel.play(self.music, loops=-1, fade_ms=1000)

    def update(self, events):
        for event in events:
            if event.type == menubutton.DrawMenu.draw(screen):
                return self.scenes['Story']
        return self

    def on_exit(self):
        self.channel.stop()


class Story(Scene):
    def __init__(self, screen, scenes):
        self.scenes = scenes
        self.screen = screen
        self.music = pygame.mixer.Sound("sad_bgm.mp3")
        self.channel = pygame.mixer.Channel(0)
        self.timer = 0

    def on_start(self):
        self.channel.play(self.music, loops=-1, fade_ms=5000)

    def update(self, events):
        if not events:
                return self.scenes['Main']

    def on_exit(self):
        self.channel.stop()


def main():
    pygame.init()
    screen = pygame.display.set_mode((900, 600), 0, 32)
    clock  = pygame.time.Clock()

    # All the scenes.
    scenes = {}
    scenes['Main'] = Main(screen, scenes)
    scenes['Story'] = Story(screen, scenes)

    # Start with the menu.
    scene = scenes['Main']
    scene.on_start()
    while True:

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return

        # Switch scenes if there is a new scene.
        new_scene = scene.update(events)
        if new_scene is not scene:
            # If there is a new scene, make sure to allow the old
            # scene to exit and the new scene to start.
            scene.on_exit()
            scene = new_scene
            scene.on_start()

        pygame.display.update()


if __name__ == '__main__':
    main()