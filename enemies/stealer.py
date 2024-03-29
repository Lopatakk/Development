from enemy import Enemy
import numpy as np
import pygame
import json
from screensetup import ScreenSetup


class Stealer(Enemy):
    def __init__(self, start, player, item):
        # reading parameters file and picking Zarovka data from it
        with open("enemies/enemyparams.json", "r") as param_file:
            enemy_param = json.load(param_file)
        param = enemy_param[3]

        super().__init__(start, "assets/images/stealer1.png", param["type"], param["hp"], param["dmg"],
                         param["explosion_size"], param["max_velocity"], param["acceleration"],
                         param["velocity_coefficient"], param["rot_velocity"], param["proj_dmg"], param["fire_rate"],
                         param["cooling"], param["overheat"], param["offset"], None, player)
        self.image_non_rot = pygame.transform.scale_by(self.image_non_rot, ScreenSetup.width/3000)
        self.item = item
        self.movement = "to_item"
        self.image_non_rot_with_medkit = pygame.image.load("assets/images/stealer2.png")
        self.image_non_rot_with_medkit = pygame.transform.scale_by(self.image_non_rot_with_medkit, ScreenSetup.width/3000)
        self.image_non_rot_with_medkit = pygame.Surface.convert_alpha(self.image_non_rot_with_medkit)

    def update(self):
        if self.movement == "to_item":
            self.item_follow(self.item.pos)
            if not self.item.alive():
                self.movement = "to_player"
        if self.movement == "to_player":
            self.follow_movement(5)
        super().update()
