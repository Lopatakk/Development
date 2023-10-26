import pygame
import numpy as np
from screen_setup import Screen_setup


class Projectile(pygame.sprite.Sprite):
    def __init__(self, picturepath, triangle):
        super().__init__()
        self.image = pygame.image.load(picturepath)
        self.rect = self.image.get_rect()
        self.rect.center = triangle.rect.center
        self.angle = triangle.angle
        self.posx = self.rect.centerx - 1/2 * triangle.triangle_width * 0.95 * np.sin(np.deg2rad(triangle.angle))
        self.posy = self.rect.centery - 1/2 * triangle.triangle_width * 0.95 * np.cos(np.deg2rad(triangle.angle))

    def update(self):
        self.posx -= np.sin(np.deg2rad(self.angle)) * 5
        self.posy -= np.cos(np.deg2rad(self.angle)) * 5
        self.rect.center = [self.posx, self.posy]
        #  kill behind borders
        if self.posx > Screen_setup.width or self.posx < 0 or self.posy > Screen_setup.height or self.posy < 0:
            self.kill()
