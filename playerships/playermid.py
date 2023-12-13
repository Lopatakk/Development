from playership import PlayerShip
from pygame.sprite import Group
import json


class PlayerMid(PlayerShip):
    def __init__(self, clock, projectile_group: Group):
        with open("playerships/playerparams.json", "r") as param_file:
            player_param = json.load(param_file)
        mid_param = player_param[1]

        super().__init__("assets/images/vlod5.png", mid_param["hp"], mid_param["dmg"],
                         mid_param["explosion_size"], mid_param["max_velocity"], mid_param["velocity_coefficient"],
                         mid_param["proj_dmg"], mid_param["fire_rate"], mid_param["cooling"], mid_param["overheat"],
                         projectile_group, clock)

    def update(self):
        super().update()
