from playership import PlayerShip
from pygame.sprite import Group
import json


class PlayerLight(PlayerShip):
    def __init__(self, clock, projectile_group: Group):
        with open("playerships/playerparams.json", "r") as param_file:
            player_param = json.load(param_file)
        light_param = player_param[0]

        super().__init__(light_param["picture_path"], light_param["hp"], light_param["dmg"],light_param["explosion_size"],
                         light_param["max_velocity"], light_param["velocity_coefficient"], light_param["proj_dmg"],
                         light_param["fire_rate"], light_param["cooling"], light_param["overheat"], projectile_group,
                         clock)

    def update(self):
        super().update()
