from playership import PlayerShip
from pygame.sprite import Group
import json


class PlayerTank(PlayerShip):
    def __init__(self, clock, projectile_group: Group):
        with open("playerships/playerparams.json", "r") as param_file:
            player_param = json.load(param_file)
        tank_param = player_param[2]

        super().__init__("assets/images/vlod5T.png", tank_param["hp"], tank_param["dmg"],
                         tank_param["explosion_size"], tank_param["max_velocity"], tank_param["velocity_coefficient"],
                         tank_param["proj_dmg"], tank_param["fire_rate"], tank_param["cooling"], tank_param["overheat"],
                         projectile_group, clock)

    def update(self):
        super().update()
