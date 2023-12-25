from enemy import Enemy
import numpy as np
import pygame
import json


class Zarovka(Enemy):
    def __init__(self, start, player):
        # reading parameters file and picking Zarovka data from it
        with open("enemies/enemyparams.json", "r") as param_file:
            enemy_param = json.load(param_file)
        param = enemy_param[0]

        super().__init__(start, "assets/images/zarovka_new.png", param["hp"], param["dmg"], param["explosion_size"],
                         param["max_velocity"], param["acceleration"], param["velocity_coefficient"],
                         param["rot_velocity"], param["proj_dmg"], param["fire_rate"], param["cooling"],
                         param["overheat"], param["offset"], None, player)

        self.image_non_rot = pygame.transform.scale_by(self.image_non_rot, 1.9)

    def update(self):
        self.follow_movement(5)
        super().update()
