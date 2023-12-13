from enemy import Enemy
import pygame
import numpy as np
from pygame.sprite import Group


class Tank(Enemy):
    def __init__(self, start, projectile_group, clock, player):
        super().__init__(start, "../assets/images/tank.png", 4000, 600, 2, 24,
                         0.1, 30, 1, 3, 100, projectile_group, clock, player)
        self.image_non_rot = pygame.transform.scale(self.image_non_rot, (150, 150))

    def update(self):
        self.shoot()
        self.follow_movement(5)
        super().update()
