import pygame
from screensetup import ScreenSetup
from ship import Ship
import numpy as np
from checkbuttons import *
from pygame.sprite import Group
import json


class PlayerShip(Ship):
    """
    The player's ship class.
    Constructor creates the ship based on parent class Ship and spawns it in the middle of the screen.
    The update() function calculates the angle between the ship and mouse positions and then calls the parent's class
    update (see Ship's update() function).
    """
    def __init__(self, picture_path, hp, dmg, explosion_size, max_velocity, acceleration, velocity_coefficient, proj_dmg,
                 fire_rate, cooling, overheat, projectile_group, clock):
        """
        :param clock: Clock object used in game
        :param projectile_group: sprite group for fired projectiles
        """
        super().__init__(np.array([ScreenSetup.width/2, ScreenSetup.height/2]), picture_path, hp, dmg, explosion_size,
                         max_velocity, acceleration, velocity_coefficient, proj_dmg, fire_rate, cooling, overheat,
                         projectile_group, clock)
        self.buttons_state = [False, False, False, False, False, False, False]

        self.last_q_use = 0
        self.q_cooldown = 10
        self.is_q_action_on = False
        self.q_ongoing_time = 5

        self.last_e_use = 0
        self.e_cooldown = 20
        self.is_e_action_on = False
        self.e_ongoing_time = 5

    def update(self):
        # angle calculation
        self.angle = self.rot_compute(self.rect.center[0] - pygame.mouse.get_pos()[0],
                                      self.rect.center[1] - pygame.mouse.get_pos()[1])

        # key/mouse pressing
        self.buttons_state = check_buttons()
        #   w s a d
        self.accelerate()
        #   q
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
        #   e
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
        #   mouse
        if self.buttons_state[6]:
            self.shoot()

        # update declared in class Ship
        super().update()

        # position limitations (borders)
        # makes sure the ship does not reach out borders of the screen, also resets the velocity in given axis
        # X
        if self.pos[0] < 0:
            self.pos[0] = 0
            self.velocity[0] = 0
        elif self.pos[0] > ScreenSetup.width:
            self.pos[0] = ScreenSetup.width
            self.velocity[0] = 0
        # Y
        if self.pos[1] < 0:
            self.pos[1] = 0
            self.velocity[1] = 0
        elif self.pos[1] > ScreenSetup.height:
            self.pos[1] = ScreenSetup.height
            self.velocity[1] = 0

    def accelerate(self):
        # X axis
        if self.buttons_state[2] and self.buttons_state[3]:
            self.velocity[0] += 0
        elif self.buttons_state[2]:
            self.velocity[0] -= self.acceleration
        elif self.buttons_state[3]:
            self.velocity[0] += self.acceleration

        # Y axis
        if self.buttons_state[0] and self.buttons_state[1]:
            self.velocity[0] += 0
        elif self.buttons_state[0]:
            self.velocity[1] -= self.acceleration
        elif self.buttons_state[1]:
            self.velocity[1] += self.acceleration

    def q_action(self):
        print("\"Q\" action not defined")

    def q_turn_off(self):
        print("\"Q\" turn off action not defined (which is probably problem)")

    def e_action(self):
        print("\"E\" action not defined")

    def e_turn_off(self):
        print("\"E\" turn off action not defined (which is probably problem)")
