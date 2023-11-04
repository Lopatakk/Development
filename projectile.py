import pygame
import numpy as np
from screensetup import ScreenSetup


class Projectile(pygame.sprite.Sprite):
    def __init__(self, picture_path, ship):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.posx = ship.rect.centerx - 1 / 2 * ship.ship_width * np.sin(np.deg2rad(ship.angle))
        self.posy = ship.rect.centery - 1 / 2 * ship.ship_width * np.cos(np.deg2rad(ship.angle))
        self.rect.center = [self.posx, self.posy]
        self.angle = ship.angle
        self.mask = pygame.mask.from_surface(self.image)
        self.velocity = 5

    damage = 20

    def update(self):
        self.posx -= np.sin(np.deg2rad(self.angle)) * self.velocity
        self.posy -= np.cos(np.deg2rad(self.angle)) * self.velocity
        self.rect.center = [self.posx, self.posy]
        #  kill behind borders
        if self.posx > ScreenSetup.width or self.posx < 0 or self.posy > ScreenSetup.height or self.posy < 0:
            self.kill()
