from enemy import Enemy
import numpy as np
import pygame
import random


class Sniper(Enemy):
    def __init__(self, start: np.ndarray, projectile_group):
        super().__init__(start, 5, "assets/images/zarovka.png", 45, 0.1, 200, 50, 0.5, 100, 1, 1, projectile_group)
        self.image_non_rot = pygame.transform.scale(self.image_non_rot, (60, 100))

    def update(self):
        super().update()
