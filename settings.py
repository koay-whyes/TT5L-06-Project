import pygame
import main
from main import soundon_img,soundoff_img,screen,BLACK

#image_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")


sound_on=True

screen.fill(BLACK)

if main.sound_button.draw(screen):
    sound_on=not sound_on

    if sound_on:
        main.sound_button.update_image(soundon_img)
        pygame.mixer.music.play(-1)
    else:
        main.sound_button.update_image(soundoff_img)
        pygame.mixer.music.stop()