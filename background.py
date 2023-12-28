import pygame
from screensetup import ScreenSetup


class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = []
        for num in range(1, 4):
            img = pygame.image.load(f"assets/animations/background/Background{num}.png")
            img = pygame.transform.scale(img, (ScreenSetup.width, ScreenSetup.height))
            img = pygame.Surface.convert(img)
            # add the image to the list
            self.images.append(img)
        self.index = 0
        self.counter = 0
        self.animation_speed = 7
        self.last_animation_time = 0
        self.time_between_animations = 3

        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = [0, 0]

    def update(self):
        self.counter += 1
        if self.counter >= self.animation_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        if self.index >= len(self.images) - 1 and self.counter >= self.animation_speed:
            self.counter = 0
            self.index = 0
        super().update()
