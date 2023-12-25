from enemy import Enemy
import pygame
import numpy as np
from pygame.sprite import Group
import json


class Tank(Enemy):
    def __init__(self, start, projectile_group, player):
        # reading parameters file and picking Tank data from it
        with open("enemies/enemyparams.json", "r") as param_file:
            enemy_param = json.load(param_file)
        param = enemy_param[1]

        super().__init__(start, "assets/images/tank.png", param["hp"], param["dmg"], param["explosion_size"],
                         param["max_velocity"], param["acceleration"], param["velocity_coefficient"],
                         param["rot_velocity"], param["proj_dmg"], param["fire_rate"], param["cooling"],
                         param["overheat"], param["offset"], projectile_group, player)

        self.proj_spawn_offset = np.array([0, - 1/1.8 * self.height])

        self.image_non_rot = pygame.transform.scale(self.image_non_rot, (150, 150))

    def update(self):
        self.shoot()
        self.follow_movement(5)
        super().update()
