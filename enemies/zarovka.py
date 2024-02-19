from enemies.enemy import Enemy
import pygame
import json
from screensetup import ScreenSetup


class Zarovka(Enemy):
    def __init__(self, start, player):
        # reading parameters file and picking Zarovka data from it
        with open("enemies/enemyparams.json", "r") as param_file:
            enemy_param = json.load(param_file)
        param = enemy_param[0]

        super().__init__(start, "assets/images/zarovka.png", param["img_scaling_coefficient"], param["shooting_ani_images"],
                         param["type"], param["hp"], param["dmg"], param["explosion_size"],
                         param["max_velocity"], param["acceleration"], param["velocity_coefficient"], param["rot_velocity"],
                         param["proj_dmg"], param["fire_rate"], param["cooling"], param["overheat"],
                         param["offset"], None, player)

    def update(self):
        self.follow_movement(5)
        super().update()
