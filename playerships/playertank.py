from playership import PlayerShip
from pygame.sprite import Group
import json
import pygame
from playerships.eventhorizonpulse import EventHorizonPulse
from screensetup import ScreenSetup


class PlayerTank(PlayerShip):
    def __init__(self, projectile_group: Group):
        # reading parameters file and picking PlayerTank data from it
        with open("playerships/playerparams.json", "r") as param_file:
            player_param = json.load(param_file)
        param = player_param[2]

        super().__init__("assets/images/vlod5T.png", param["hp"], param["dmg"], param["explosion_size"],
                         param["max_velocity"], param["acceleration"], param["velocity_coefficient"], param["proj_dmg"],
                         param["fire_rate"], param["cooling"], param["overheat"], param["q_cooldown"],
                         param["q_ongoing_time"], param["e_cooldown"], param["e_ongoing_time"], projectile_group)
        self.type = "player"
        self.speed_boost_sound = pygame.mixer.Sound("assets/sounds/speed_boost.mp3")
        self.speed_boost_sound.set_volume(0.4)
        self.speed_boost_off_sound = pygame.mixer.Sound("assets/sounds/speed_boost_off.mp3")
        self.speed_boost_off_sound.set_volume(0.3)

        self.event_horizon_pulse = None
        self.screen = ScreenSetup.screen

    def update(self):
        super().update()

    def q_action(self):
        self.acceleration = 2.5 * self.acceleration
        self.max_velocity = 2 * self.max_velocity
        pygame.mixer.find_channel(True).play(self.speed_boost_sound)

    def q_turn_off(self):
        self.acceleration = 1/2.5 * self.acceleration
        self.max_velocity = 1/2 * self.max_velocity
        pygame.mixer.find_channel(True).play(self.speed_boost_off_sound)

    def e_action(self):
        self.event_horizon_pulse = EventHorizonPulse(self)
        self.projectile_group.add(self.event_horizon_pulse)

    def e_turn_off(self):
        self.event_horizon_pulse.destroy()
