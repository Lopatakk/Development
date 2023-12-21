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

    def update(self):
        # angle calculation
        self.angle = self.rot_compute(self.rect.center[0] - pygame.mouse.get_pos()[0],
                                      self.rect.center[1] - pygame.mouse.get_pos()[1])

        # key/mouse pressing
        self.buttons_state = check_buttons()
        self.accelerate()
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
