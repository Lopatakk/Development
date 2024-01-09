from playership import PlayerShip
from pygame.sprite import Group
import json
import pygame
from playerships.eventhorizonpulse import EventHorizonPulse
from screensetup import ScreenSetup
from projectile import Projectile


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

        super().__init__("assets/images/vlod5T.png", param["type"], param["hp"], param["dmg"], param["explosion_size"],
                         param["max_velocity"], param["acceleration"], param["velocity_coefficient"], param["proj_dmg"],
                         param["fire_rate"], param["cooling"], param["overheat"], param["q_cooldown"],
                         param["q_ongoing_time"], param["e_cooldown"], param["e_ongoing_time"], projectile_group)

        # image scaling
        self.image_non_rot = pygame.transform.scale_by(self.image_non_rot, ScreenSetup.width / 1920 * 5/6)
        self.width, self.height = self.image.get_width(), self.image.get_height()

        # q action variables and setup
        self.speed_boost_sound = pygame.mixer.Sound("assets/sounds/speed_boost.mp3")
        self.speed_boost_sound.set_volume(0.4)
        self.speed_boost_off_sound = pygame.mixer.Sound("assets/sounds/speed_boost_off.mp3")
        self.speed_boost_off_sound.set_volume(0.3)

        # e action variables and setup
        self.event_horizon_pulse = None
        self.screen = ScreenSetup.screen

        # shooting animation setup
        self.image_non_rot_orig = self.image_non_rot
        self.shooting_image = pygame.image.load(f"assets/animations/shooting/TANK/TANK1.png")
        self.shooting_image = pygame.transform.scale_by(self.shooting_image, ScreenSetup.width / 1920 * 5/6)
        self.index = 0
        self.counter = -1
        self.animation_speed = 3

    def update(self):
        """
        Customized update function including shooting animation and shield functionality unlike the PlayerShip update.
        :return: None
        """
        # shooting animation
        if self.counter >= 0:
            self.counter += 1
        if self.counter >= self.animation_speed:
            # changing the image back
            self.image_non_rot = self.image_non_rot_orig
            self.counter = -1
            # firing from the gun
            projectile = Projectile(self)
            self.projectile_group.add(projectile)

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

    def shoot(self):
        """
        If the time after last shot is larger than self.fire_rate_time and the gun is not overheated, this function
        heats the gun and starts the shooting animation by setting the counter to 0. At the end of the animation is
        created a projectile.
        :return: None
        """
        elapsed_time = self.time_alive - self.last_shot_time
        if elapsed_time >= self.fire_rate_time and not self.is_overheated:
            self.last_shot_time = self.time_alive
            self.heat += 1

            self.counter = 0
            self.image_non_rot = self.shooting_image
