from enemy import Enemy
import pygame
import numpy as np
from pygame.sprite import Group
import json
from screensetup import ScreenSetup
from projectile import Projectile


class Tank(Enemy):
    def __init__(self, start, projectile_group, player):
        # reading parameters file and picking Tank data from it
        with open("enemies/enemyparams.json", "r") as param_file:
            enemy_param = json.load(param_file)
        param = enemy_param[1]

        super().__init__(start, "assets/images/tank.png", param["shooting_ani_images"], param["type"], param["hp"], param["dmg"],
                         param["explosion_size"], param["max_velocity"], param["acceleration"],
                         param["velocity_coefficient"], param["rot_velocity"], param["proj_dmg"], param["fire_rate"],
                         param["cooling"], param["overheat"], param["offset"], projectile_group, player)

        scale_ratio = ScreenSetup.width / 1800
        self.image_non_rot_orig = pygame.transform.scale_by(self.image_non_rot_orig, scale_ratio)
        self.image_non_rot = pygame.transform.scale_by(self.image_non_rot, scale_ratio)
        for num in range(len(self.ani_shooting_images)):
            self.ani_shooting_images[num] = pygame.transform.scale_by(self.ani_shooting_images[num], scale_ratio)
        self.width, self.height = self.image_non_rot_orig.get_width(), self.image_non_rot_orig.get_height()

        self.proj_spawn_offset = np.array([0, -1/2 * self.height])

    def update(self):
        self.shoot()
        self.follow_movement(5)

        super().update()
