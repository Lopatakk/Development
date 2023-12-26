from enemy import Enemy
import numpy as np
import pygame
import json


class Stealer(Enemy):
    def __init__(self, start, player, item_group):
        self.player = player
        self.item_group = item_group
        self.item = None
        for sprite in self.item_group.sprites():
                self.item = sprite

        # reading parameters file and picking Zarovka data from it
        with open("enemies/enemyparams.json", "r") as param_file:
            enemy_param = json.load(param_file)
        param = enemy_param[3]

        super().__init__(start, "assets/images/zarovka.png", param["type"], param["hp"], param["dmg"],
                         param["explosion_size"], param["max_velocity"], param["acceleration"],
                         param["velocity_coefficient"], param["rot_velocity"], param["proj_dmg"], param["fire_rate"],
                         param["cooling"], param["overheat"], param["offset"], None, player)
        self.movement = "movement1"
        self.image_non_rot = pygame.transform.scale_by(self.image_non_rot, (150, 150))

    def update(self):

        if self.movement == "movement1":
            self.item_follow(self.item.pos)
        if self.movement == "movement2":
            self.follow_movement(5)
        super().update()
