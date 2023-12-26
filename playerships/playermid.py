import pygame.mixer
from playerships.blast import Blast
from playership import PlayerShip
from pygame.sprite import Group
import json
import numpy as np


class PlayerMid(PlayerShip):
    def __init__(self, projectile_group: Group):
        # reading parameters file and picking PlayerMid data from it
        with open("playerships/playerparams.json", "r") as param_file:
            player_param = json.load(param_file)
        param = player_param[1]

        super().__init__("assets/images/vlod5.png", param["hp"], param["dmg"], param["explosion_size"],
                         param["max_velocity"], param["acceleration"], param["velocity_coefficient"], param["proj_dmg"],
                         param["fire_rate"], param["cooling"], param["overheat"], param["q_cooldown"],
                         param["q_ongoing_time"], param["e_cooldown"], param["e_ongoing_time"], projectile_group)
        self.type = "player"
        self.gun_upgrade_sound = pygame.mixer.Sound("assets/sounds/gun_upgrade.mp3")
        self.gun_upgrade_sound.set_volume(0.6)

    def update(self):
        super().update()

    def q_action(self):
        self.fire_rate_time = self.fire_rate_time / 2
        self.cooling = self.cooling * 2.5
        pygame.mixer.find_channel(True).play(self.gun_upgrade_sound)

    def q_turn_off(self):
        self.fire_rate_time = self.fire_rate_time * 2
        self.cooling = self.cooling / 2.5

    def e_action(self):
        blast = Blast(self)
        self.projectile_group.add(blast)

    def e_turn_off(self):
        pass
