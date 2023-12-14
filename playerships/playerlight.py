from playership import PlayerShip
from pygame.sprite import Group
import json


class PlayerLight(PlayerShip):
    def __init__(self, clock, projectile_group: Group):
        # reading parameters file and picking PlayerLight data from it
        with open("playerships/playerparams.json", "r") as param_file:
            player_param = json.load(param_file)
        param = player_param[0]

        super().__init__("assets/images/vlod5L.png", param["hp"], param["dmg"], param["explosion_size"],
                         param["max_velocity"], param["acceleration"], param["velocity_coefficient"], param["proj_dmg"],
                         param["fire_rate"], param["cooling"], param["overheat"], projectile_group, clock)

    def update(self):
        super().update()
