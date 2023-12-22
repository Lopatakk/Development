from playership import PlayerShip
from pygame.sprite import Group
import json


class PlayerMid(PlayerShip):
    def __init__(self, clock, projectile_group: Group):
        # reading parameters file and picking PlayerMid data from it
        with open("playerships/playerparams.json", "r") as param_file:
            player_param = json.load(param_file)
        param = player_param[1]

        super().__init__("assets/images/vlod5.png", param["hp"], param["dmg"], param["explosion_size"],
                         param["max_velocity"], param["acceleration"], param["velocity_coefficient"], param["proj_dmg"],
                         param["fire_rate"], param["cooling"], param["overheat"], param["q_cooldown"],
                         param["q_ongoing_time"], param["e_cooldown"], param["e_ongoing_time"], projectile_group, clock)

    def update(self):
        super().update()

    def q_action(self):
        print("status quo")

    def q_turn_off(self):
        print("q turning off, over")

    def e_action(self):
        print("reeeeeeeeeeeee")

    def e_turn_off(self):
        print("e turning off, over")
