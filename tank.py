from enemy import Enemy
import pygame
import numpy as np
from pygame.sprite import Group


class Tank(Enemy):
    def __init__(self, start: np.ndarray, projectile_group: Group):
        super().__init__(start, 8, "assets/images/tank.png", 24, 0.1, 4500, 600, 2, 20, 100, 3, projectile_group)
        self.image_non_rot = pygame.transform.scale(self.image_non_rot, (150, 150))
    def update(self):
        self.shoot()

        super().update()
