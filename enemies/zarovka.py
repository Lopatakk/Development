from enemy import Enemy
import numpy as np
import pygame
import json
from screensetup import ScreenSetup


class Zarovka(Enemy):
    def __init__(self, start, player):
        # reading parameters file and picking Zarovka data from it
        with open("enemies/enemyparams.json", "r") as param_file:
            enemy_param = json.load(param_file)
        param = enemy_param[0]

        super().__init__(start, "assets/images/zarovka.png", param["shooting_ani_images"], param["type"], param["hp"], param["dmg"],
                         param["explosion_size"], param["max_velocity"], param["acceleration"],
                         param["velocity_coefficient"], param["rot_velocity"], param["proj_dmg"], param["fire_rate"],
                         param["cooling"], param["overheat"], param["offset"], None, player)
        scale_ratio = ScreenSetup.width/3500
        self.image_non_rot_orig = pygame.transform.scale_by(self.image_non_rot_orig, scale_ratio)
        self.image_non_rot = pygame.transform.scale_by(self.image_non_rot, scale_ratio)
        self.height = self.image_non_rot_orig.get_height()
        self.width = self.image_non_rot_orig.get_width()

    def update(self):
        self.follow_movement(5)
        super().update()
