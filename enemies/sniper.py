from enemy import Enemy
import numpy as np
import pygame
import random
from playership import PlayerShip
import json


class Sniper(Enemy):
    def __init__(self, start, projectile_group, clock, player):
        # reading parameters file and picking Sniper data from it
        with open("enemies/enemyparams.json", "r") as param_file:
            enemy_param = json.load(param_file)
        param = enemy_param[2]

        super().__init__(start, "assets/images/zarovka.png", param["hp"], param["dmg"], param["explosion_size"],
                         param["max_velocity"], param["velocity_coefficient"], param["proj_dmg"], param["fire_rate"],
                         param["cooling"], param["overheat"], projectile_group, clock, player)

        self.image_non_rot = pygame.transform.scale(self.image_non_rot, (60, 100))

        self.rot_direction = random.choice([1, -1])

    def update(self):
        self.angle_speed(self.rot_direction, 3)
        self.follow_movement_with_offset(500)
        self.shoot()
        super().update()
