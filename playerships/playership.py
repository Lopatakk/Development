import pygame
from screensetup import ScreenSetup
from ship import Ship
import numpy as np
from checkbuttons import *


class PlayerShip(Ship):
    """
    The player-type ship class.
    Constructor creates the ship based on parent class Ship and spawns it in the middle of the screen. The angle of the
    ship is calculated between the ship and mouse positions. Ships based on this class collect import from keyboard (q,
    w, e, a, s and d keys) and can have special actions that can be initialized by pressing q and e keys on keyboard,
    unlike other ships. These functions are both divided into two, turn-on and turn-off, turn-on starts when the key is
    pressed; turn-off starts when the function is on for x_ongoing_time. These actions have to be redefined in a child
    class based on this class.
    """
    def __init__(self, picture_path, img_scaling_coefficient, ani_amount_of_images,
                 ship_type, hp, dmg, explosion_size,
                 max_velocity, acceleration, velocity_coefficient,
                 proj_dmg, fire_rate, cooling, overheat,
                 q_cooldown: float, q_ongoing_time: float, e_cooldown: float, e_ongoing_time: float,
                 projectile_group) -> "PlayerShip":
        """
        :param picture_path: directory path to the ship picture
        :param img_scaling_coefficient: used to calculate scaling factor by dividing screen width with it
        :param ani_amount_of_images: number of images in the shooting animation
        :param ship_type: type of the ship
        :param hp: maximum amount of health points
        :param dmg: damage to other ships when ramming
        :param explosion_size: the size of the explosion when the ship is destroyed (see explosion.py for more)
        :param max_velocity: maximum speed the ship can travel in one axis
        :param acceleration: acceleration of the ship, is not used directly in the Ship class, but when defying movement functions in child class
        :param velocity_coefficient: enables greater range of speed, recommended value: 0.1
        :param proj_dmg: fired projectiles damage
        :param fire_rate: how many projectiles can be fired within one second
        :param cooling: how much of the heat the gun looses every second
        :param overheat: maximum amount of heat the gun can stand
        :param q_cooldown: minimal time in seconds between uses of the q action
        :param q_ongoing_time: time in seconds when the q action is active
        :param e_cooldown: minimal time in seconds between uses of the e action
        :param e_ongoing_time: time in seconds when the e action is active
        :param projectile_group: sprite group for fired projectiles
        :return: Player-type Ship object
        """

        # super().__init__ - creates a Ship object
        super().__init__(np.array([ScreenSetup.width/2, ScreenSetup.height/2]),
                         picture_path, img_scaling_coefficient, ani_amount_of_images,
                         ship_type, hp, dmg, explosion_size, max_velocity, acceleration, velocity_coefficient,
                         proj_dmg, fire_rate, cooling, overheat, projectile_group)

        # adjustment of values

        # updated value of proj_spawn_offset for player-type ships
        self.proj_spawn_offset = np.array([0, - 1/2.8 * self.height])

        # buttons states

        # buttons_state - list with up, down, left, right, function_1, function_2 and mouse_left keys/button states
        self.buttons_state = [False, False, False, False, False, False, False]

        # q action variables

        # last_q_use - in-game time when q action was lastly used, updates at the ending of the action
        self.last_q_use = 0
        # q_cooldown - minimal time in seconds between uses of the q action
        self.q_cooldown = q_cooldown
        # is_q_action_on - bool, indicates, if the q action is being used or not
        self.is_q_action_on = False
        # q_ongoing_time - time in seconds, how long is the q action active
        self.q_ongoing_time = q_ongoing_time

        # e action variables

        # last_e_use - in-game time when e action was lastly used, updates at the ending of the action
        self.last_e_use = 0
        # e_cooldown - minimal time in seconds between uses of the e action
        self.e_cooldown = e_cooldown
        # is_e_action_on - bool, indicates, if the e action is being used or not
        self.is_e_action_on = False
        # e_ongoing_time - time in seconds, how long is the e action active
        self.e_ongoing_time = e_ongoing_time

        # q and e action icons
        # loading q and e action icons for specific ship

        ScreenSetup.q_action_icon_off = pygame.image.load(f"assets/icons/{self.type}/q_off.png")
        ScreenSetup.q_action_icon_off = pygame.transform.scale_by(ScreenSetup.q_action_icon_off, 2/1920 * ScreenSetup.width)
        ScreenSetup.q_action_icon_off = pygame.Surface.convert_alpha(ScreenSetup.q_action_icon_off)

        ScreenSetup.q_action_icon_on = pygame.image.load(f"assets/icons/{self.type}/q_on.png")
        ScreenSetup.q_action_icon_on = pygame.transform.scale_by(ScreenSetup.q_action_icon_on, 2/1920 * ScreenSetup.width)
        ScreenSetup.q_action_icon_on = pygame.Surface.convert_alpha(ScreenSetup.q_action_icon_on)

        ScreenSetup.e_action_icon_off = pygame.image.load(f"assets/icons/{self.type}/e_off.png")
        ScreenSetup.e_action_icon_off = pygame.transform.scale_by(ScreenSetup.e_action_icon_off, 2/1920 * ScreenSetup.width)
        ScreenSetup.e_action_icon_off = pygame.Surface.convert_alpha(ScreenSetup.e_action_icon_off)

        ScreenSetup.e_action_icon_on = pygame.image.load(f"assets/icons/{self.type}/e_on.png")
        ScreenSetup.e_action_icon_on = pygame.transform.scale_by(ScreenSetup.e_action_icon_on, 2/1920 * ScreenSetup.width)
        ScreenSetup.e_action_icon_on = pygame.Surface.convert_alpha(ScreenSetup.e_action_icon_on)

    def update(self) -> None:
        """
        Uses the update from Ship class + processes player input (including q and e functions (both turn-on and
        turn-off for each)) and limits the ship position to screen borders.
        :return: None
        """
        # angle calculation

        # calculating the angle between ship center and mouse positions
        self.angle = self.rot_compute(self.rect.center[0] - pygame.mouse.get_pos()[0],
                                      self.rect.center[1] - pygame.mouse.get_pos()[1])

        # key/mouse pressing

        # this line gets states of all the needed buttons
        self.buttons_state = check_buttons()

        # usage of the button input

        #   w, s, a, d
        #   changes the ship velocity based on the key input
        self.accelerate()

        #   q
        #   takes care of turning on the q function when q is pressed (and cooldown is exceeded) and off after defined
        #   amount of time
        #       turn on
        if self.buttons_state[4]:
            elapsed_time = self.time_alive - self.last_q_use
            if elapsed_time >= self.q_cooldown:
                self.q_action()
                self.is_q_action_on = True
                self.last_q_use = self.time_alive
        #       turn off
        if self.is_q_action_on and self.time_alive >= self.last_q_use + self.q_ongoing_time:
            self.q_turn_off()
            self.is_q_action_on = False
            self.last_q_use = self.time_alive
        #   e
        #   takes care of turning on the e function when e is pressed (and cooldown is exceeded) and off after defined
        #   amount of time
        #       turn on
        if self.buttons_state[5]:
            elapsed_time = self.time_alive - self.last_e_use
            if elapsed_time >= self.e_cooldown:
                self.e_action()
                self.is_e_action_on = True
                self.last_e_use = self.time_alive
        #       turn off
        if self.is_e_action_on and self.time_alive >= self.last_e_use + self.e_ongoing_time:
            self.e_turn_off()
            self.is_e_action_on = False
            self.last_e_use = self.time_alive

        #   mouse
        #   tries to shoot when the left mouse button is pressed
        if self.buttons_state[6]:
            self.shoot()

        # super().update() - update declared in class Ship
        super().update()

        # position limitations (borders)

        # makes sure the ship does not reach out borders of the screen, resets the velocity in given axis when the
        # border is reached
        #   X axis
        if self.pos[0] < 0:
            self.pos[0] = 0
            self.velocity[0] = 0
        elif self.pos[0] > ScreenSetup.width:
            self.pos[0] = ScreenSetup.width
            self.velocity[0] = 0
        #   Y axis
        if self.pos[1] < 0:
            self.pos[1] = 0
            self.velocity[1] = 0
        elif self.pos[1] > ScreenSetup.height:
            self.pos[1] = ScreenSetup.height
            self.velocity[1] = 0

    def accelerate(self) -> None:
        """
        Uses the keyboard input to change ship velocity in axes by the acceleration value. If both keys in the same axis
        are pressed (for example, a and d), the velocity does not change.
        :return: None
        """
        # X-axis
        #   both keys pressed
        if self.buttons_state[2] and self.buttons_state[3]:
            self.velocity[0] += 0
        #   a key pressed
        elif self.buttons_state[2]:
            self.velocity[0] -= self.acceleration
        #   d key pressed
        elif self.buttons_state[3]:
            self.velocity[0] += self.acceleration

        # Y-axis
        #   both keys pressed
        if self.buttons_state[0] and self.buttons_state[1]:
            self.velocity[0] += 0
        #   w key pressed
        elif self.buttons_state[0]:
            self.velocity[1] -= self.acceleration
        #   s key pressed
        elif self.buttons_state[1]:
            self.velocity[1] += self.acceleration

    # q nad e actions and turn-off actions

    # redefine these in child classes, so it can actually do something :)
    def q_action(self) -> None:
        """
        Prints the statement "Q action not defined", to warn the user of the ship.
        :return: None
        """
        print("\"Q\" action not defined")

    def q_turn_off(self) -> None:
        """
        Prints the statement "Q turn off action not defined", to warn the user of the ship.
        :return: None
        """
        print("\"Q\" turn off action not defined")

    def e_action(self) -> None:
        """
        Prints the statement "E action not defined", to warn the user of the ship.
        :return: None
        """
        print("\"E\" action not defined")

    def e_turn_off(self) -> None:
        """
        Prints the statement "E turn off action not defined", to warn the user of the ship.
        :return: None
        """
        print("\"E\" turn off action not defined")
