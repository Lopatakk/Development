import pygame
import numpy as np
from screensetup import ScreenSetup
from projectile import Projectile


class Ship(pygame.sprite.Sprite):
    def __init__(self, picture_path, start_pos_x, start_pos_y):
        super().__init__()
        # health
        self.hp = 100

        # image
        self.image_non_rot = pygame.image.load(picture_path)
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.ship_width = self.rect.height
        self.mask = pygame.mask.from_surface(self.image)

        # position
        self.pos = np.array([start_pos_x, start_pos_y])

        # angle
        self.angle = 0

        # velocity
        self.velocity = np.array([0, 0])
        self.max_velocity = np.array([100, 100])
        self.velocity_coefficient = 0.1

        # spawn point
        self.rect.center = [ScreenSetup.width / 2, ScreenSetup.height / 2]

        # projectiles
        self.damage = 20

    def update(self):
        # rotation
        # angle must be calculated before calling the super().update() function!
        self.image = pygame.transform.rotate(self.image_non_rot, self.angle)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        # max speed limitations
        if self.velocity[0] > self.max_velocity[0]:
            self.velocity[0] = self.max_velocity[0]
        elif self.velocity[0] < -self.max_velocity[0]:
            self.velocity[0] = -self.max_velocity[0]
        if self.velocity[1] > self.max_velocity[1]:
            self.velocity[1] = self.max_velocity[1]
        elif self.velocity[1] < -self.max_velocity[1]:
            self.velocity[1] = -self.max_velocity[1]

        # movement
        self.pos[0] += self.velocity[0] * self.velocity_coefficient
        self.pos[1] += self.velocity[1] * self.velocity_coefficient

        # position update
        self.rect.center = self.pos

    # rotation computing
    @classmethod
    def rot_compute(cls, dist_x, dist_y):
        if dist_y > 0:
            return np.rad2deg(np.arctan(dist_x/dist_y))
        elif dist_y < 0:
            return 180 + np.rad2deg(np.arctan(dist_x/dist_y))
        else:
            if dist_x > 0:
                return 90
            else:
                return -90

    # shooting
    def shoot(self):
        projectile = Projectile("projectile.png", self)
        return projectile
