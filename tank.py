from enemy import Enemy
import pygame
import numpy as np
from pygame.sprite import Group


class Tank(Enemy):
    def __init__(self, start: np.ndarray, clock, projectile_group: Group, player):
        super().__init__(start, 8, "assets/images/tank.png", clock, 24, 0.1, 4500, 600, 2, 50, projectile_group, 100, 3, 2, player)
        self.image_non_rot = pygame.transform.scale(self.image_non_rot, (150, 150))

    def update(self):
        self.shoot()
        self.follow_movement()
        super().update()
