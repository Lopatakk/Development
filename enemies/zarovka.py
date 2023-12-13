from enemy import Enemy
import numpy as np
import pygame
import json


class Zarovka(Enemy):
    def __init__(self, start, clock, player):
        with open("enemies/enemyparams.json", "r") as param_file:
            enemy_param = json.load(param_file)
        param = enemy_param[0]

        super().__init__(start, "assets/images/zarovka_new.png", param["hp"], param["dmg"], param["explosion_size"],
                         param["max_velocity"], param["velocity_coefficient"], param["proj_dmg"], param["fire_rate"],
                         param["cooling"], param["overheat"], None, clock, player)

        self.image_non_rot = pygame.transform.scale(self.image_non_rot, (120, 120))

    def update(self):
        self.follow_movement(5)
        super().update()
