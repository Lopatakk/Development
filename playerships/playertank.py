from playerships.playership import PlayerShip
from pygame.sprite import Group
import json
import pygame
from playerships.eventhorizonpulse import EventHorizonPulse
from screensetup import ScreenSetup


class PlayerTank(PlayerShip):
    """
    It's strong and thick armor guarantee good defense and a lot of hp. The fast-firing cannon with lowered damage
    destroys enemies in a moment. Unfortunately, heavy armor and gun usually result in a bad manoeuvrability, and this
    ship is not an exception, so try to destroy your enemies as soon as you see them.
    Q action: speed boost - increases acceleration and top speed
    E action: event horizon pulse - emits a very strong gravitational wave around the ship, which destroys everything it
    touches
    """
    def __init__(self, projectile_group: Group):
        """
        :param projectile_group: sprite group for fired projectiles
        """
        # reading parameter file and picking PlayerTank data from it
        with open("playerships/playerparams.json", "r") as param_file:
            player_param = json.load(param_file)
        param = player_param[2]
        image = pygame.image.load("assets/images/player_tank/vlod_player_tank.png")

        super().__init__(image, param["img_scaling_coefficient"], param["shooting_ani_images"],
                         param["type"], param["hp"], param["dmg"], param["explosion_size"], param["regeneration"],
                         param["max_velocity"], param["acceleration"], param["velocity_coefficient"],
                         param["proj_dmg"], param["fire_rate"], param["cooling"], param["overheat"],
                         param["q_cooldown"], param["q_ongoing_time"], param["e_cooldown"], param["e_ongoing_time"],
                         False, projectile_group)

        # q action variables and setup
        self.speed_boost_sound = pygame.mixer.Sound("assets/sounds/speed_boost.mp3")
        self.speed_boost_sound.set_volume(0.4 * ScreenSetup.effects_volume)
        self.speed_boost_off_sound = pygame.mixer.Sound("assets/sounds/speed_boost_off.mp3")
        self.speed_boost_off_sound.set_volume(0.3 * ScreenSetup.effects_volume)

        # e action variables and setup
        self.event_horizon_pulse = None
        self.screen = ScreenSetup.screen

    def update(self):
        """
        Customized update function including shooting animation and shield functionality unlike the PlayerShip update.
        :return: None
        """
        super().update()

    def q_action(self):
        """
        Speed boost start, the ship is faster.
        :return: None
        """
        self.acceleration = 2.5 * self.acceleration
        self.max_velocity = 2 * self.max_velocity
        pygame.mixer.find_channel(False).play(self.speed_boost_sound)

    def q_turn_off(self):
        """
        Speed boost end, the ship is as fast as normally.
        :return: None
        """
        self.acceleration = 1/2.5 * self.acceleration
        self.max_velocity = 1/2 * self.max_velocity
        pygame.mixer.find_channel(False).play(self.speed_boost_off_sound)

    def e_action(self):
        """
        Event horizon pulse emitting, creates the pulse.
        :return: None
        """
        self.event_horizon_pulse = EventHorizonPulse(self)
        self.projectile_group.add(self.event_horizon_pulse)

    def e_turn_off(self):
        """
        Event horizon pulse end, destroys the pulse.
        :return: None
        """
        self.event_horizon_pulse.kill()
