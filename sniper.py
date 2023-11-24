from enemy import Enemy
import numpy as np
import pygame
import random
from player_ship import PlayerShip


class Sniper(Enemy):
    def __init__(self, start: np.ndarray, projectile_group):
        super().__init__(start, 5, "assets/images/zarovka.png", 45, 0.1, 200, 50, 0.5, 0, projectile_group, 1, 1, 2)
        self.image_non_rot = pygame.transform.scale(self.image_non_rot, (60, 100))

    def update(self, player_pos):
        self.follow_movement_with_offset(player_pos, 550, 10)
        self.shoot()
        super().update()
