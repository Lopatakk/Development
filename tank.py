from enemy import Enemy
import pygame
import numpy as np
from pygame.sprite import Group


class Tank(Enemy):
    def __init__(self, start: np.ndarray, projectile_group: Group):
        super().__init__(start, 8, "assets/images/tank.png", 30, 0.1, 4500, 1000, 0.5, 20, projectile_group)

    def update(self):
        current_time = pygame.time.get_ticks()

        self.shoot()

        super().update()
