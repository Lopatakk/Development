from enemy import Enemy
import numpy as np
import pygame
import random
from player_ship import PlayerShip


class Sniper(Enemy):
    def __init__(self, start: np.ndarray, clock, projectile_group, player):
        super().__init__(start, 5, "assets/images/zarovka.png", clock, 45, 0.1, 200, 150, 0.5, 150, projectile_group, 1, 1, 2, player)
        self.image_non_rot = pygame.transform.scale(self.image_non_rot, (60, 100))
        self.rot_direction = random.choice([1, -1])

    def update(self):
        self.angle_speed(self.rot_direction)
        self.follow_movement_with_offset(500)
        self.shoot()
        super().update()
