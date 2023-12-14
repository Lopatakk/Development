from playership import PlayerShip
from pygame.sprite import Group
import json


class PlayerTank(PlayerShip):
    def __init__(self, clock, projectile_group: Group):
        # reading parameters file and picking PlayerTank data from it
        with open("playerships/playerparams.json", "r") as param_file:
            player_param = json.load(param_file)
        param = player_param[2]

        super().__init__("assets/images/vlod5T.png", param["hp"], param["dmg"], param["explosion_size"],
                         param["max_velocity"], param["acceleration"], param["velocity_coefficient"], param["proj_dmg"],
                         param["fire_rate"], param["cooling"], param["overheat"], projectile_group, clock)

    def update(self):
        super().update()
