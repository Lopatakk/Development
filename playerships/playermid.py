from playership import PlayerShip
from pygame.sprite import Group
import json


class PlayerMid(PlayerShip):
    def __init__(self, clock, projectile_group: Group):
        with open("playerships/playerparams.json", "r") as param_file:
            player_param = json.load(param_file)
        param = player_param[1]

        super().__init__("assets/images/vlod5.png", param["hp"], param["dmg"], param["explosion_size"],
                         param["max_velocity"], param["velocity_coefficient"], param["proj_dmg"], param["fire_rate"],
                         param["cooling"], param["overheat"], projectile_group, clock)

    def update(self):
        super().update()
