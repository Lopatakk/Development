from enemy import Enemy
import numpy as np
import pygame
import random
from playership import PlayerShip


class Sniper(Enemy):
    def __init__(self, start, projectile_group, clock, player):
        super().__init__(start, "../assets/images/zarovka.png", 200, 150, 2, 45,
                         0.1, 150, 0.5, 1, 1, projectile_group, clock, player)
        self.image_non_rot = pygame.transform.scale(self.image_non_rot, (60, 100))
        self.rot_direction = random.choice([1, -1])

    def update(self):
        self.angle_speed(self.rot_direction, 3)
        self.follow_movement_with_offset(500)
        self.shoot()
        super().update()
