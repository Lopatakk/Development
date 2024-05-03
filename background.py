import pygame
from screensetup import ScreenSetup
import random


class Background(pygame.sprite.Sprite):
    def __init__(self, background_type, frames_num, rand):
        super().__init__()
        self.images = []
        for num in range(frames_num):
            img = pygame.image.load(f"assets/animations/background/{background_type}{num}.png").convert_alpha()
            img = pygame.transform.scale(img, (ScreenSetup.width, ScreenSetup.height))
            img = pygame.Surface.convert(img)
            # add the image to the list
            self.images.append(img)
        self.counter = 0
        self.animation_speed = random.randint(rand[0], rand[1])

        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = [0, 0]

    def update(self):
        self.counter += 1
        if self.counter >= self.animation_speed:
            index = random.randint(0, len(self.images) - 1)
            self.image = self.images[index]
            self.animation_speed = random.randint(50, 100)
            self.counter = 0
        super().update()

