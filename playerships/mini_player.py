from playerships.playermid import PlayerMid
from pygame.sprite import Group
import pygame
import json


class MiniPlayer(PlayerMid):
    """
    Mini version of middle classed ship with balanced properties. Not so light armor, quite good manoeuvrability and a relatively
    powerful gun results in a universal machine that can withstand some damage as well as fly away from its enemies and
    kill them while doing so. There is nothing to recommend you, try your best!
    Q action: rapid fire - increases fire rate and cooling
    E action: blast - fires a big projectile, which destroys everything in its path
    """
    def __init__(self, projectile_group: Group):
        self.mini = True

        with open("playerships/miniplayerparams.json", "r") as param_file:
            player_param = json.load(param_file)
        param = player_param
        image = pygame.image.load("assets/images/cockpit/vlod_player_mid.png").convert_alpha()
        super().__init__(projectile_group, self.mini, image, param["img_scaling_coefficient"], param["shooting_ani_images"],
                         param["type"], param["hp"], param["dmg"], param["explosion_size"], param["regeneration"],
                         param["max_velocity"], param["acceleration"], param["velocity_coefficient"],
                         param["proj_dmg"], param["fire_rate"], param["cooling"], param["overheat"],
                         param["q_cooldown"], param["q_ongoing_time"], param["e_cooldown"], param["e_ongoing_time"])

    def update(self):
        """
        Customized update function including shooting animation unlike the PlayerShip update.
        :return: None
        """
        super().update()
