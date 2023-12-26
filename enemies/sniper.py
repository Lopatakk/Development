from enemy import Enemy
import numpy as np
import pygame
import random
from playership import PlayerShip
import json


class Sniper(Enemy):
    def __init__(self, start, projectile_group, player):
        # reading parameters file and picking Sniper data from it
        with open("enemies/enemyparams.json", "r") as param_file:
            enemy_param = json.load(param_file)
        param = enemy_param[2]

        super().__init__(start, "assets/images/sniper.png", param["hp"], param["dmg"], param["explosion_size"],
                         param["max_velocity"], param["acceleration"], param["velocity_coefficient"],
                         param["rot_velocity"], param["proj_dmg"], param["fire_rate"], param["cooling"],
                         param["overheat"], param["offset"], projectile_group, player)

        self.proj_spawn_offset = np.array([0, - 1/1.95 * self.height])

        self.rot_direction = random.choice([1, -1])

    def update(self):
        self.angle_speed(self.rot_direction)
        self.follow_movement_with_offset()
        self.shoot()
        super().update()
