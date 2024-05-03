from enemies.zarovka import Zarovka
from pygame.sprite import Group
import pygame
import json


class MiniZarovka(Zarovka):
    def __init__(self, start, player):
        self.mini = True

        with open("enemies/minienemyparams.json", "r") as param_file:
            player_param = json.load(param_file)
        param = player_param[0]
        image = pygame.image.load("assets/images/cockpit/zarovka.png").convert_alpha()
        super().__init__(start, player, self.mini, image, param["img_scaling_coefficient"], param["shooting_ani_images"],
                         param["type"], param["hp"], param["dmg"], param["explosion_size"],
                         param["max_velocity"], param["acceleration"], param["velocity_coefficient"], param["rot_velocity"],
                         param["proj_dmg"], param["fire_rate"], param["cooling"], param["overheat"],
                         param["offset"])

    def update(self):
        """
        Customized update function including shooting animation unlike the PlayerShip update.
        :return: None
        """
        super().update()
