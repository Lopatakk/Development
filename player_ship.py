import pygame
from screensetup import ScreenSetup
from ship import Ship
import numpy as np
from checkbuttons import *
from pygame.sprite import Group


class PlayerShip(Ship):
    """
    The player's ship class.
    Constructor creates the ship based on parent class Ship and spawns it in the middle of the screen.
    The update() function calculates the angle between the ship and mouse positions and then calls the parent's class
    update (see Ship's update() function).
    """
    def __init__(self, clock, projectile_group: Group):
        """
        :param clock: Clock object used in game
        :param projectile_group: sprite group for fired projectiles
        """
        super().__init__("assets/images/vlod5.png", clock, np.array([ScreenSetup.width/2, ScreenSetup.height/2]),
                         100, 0.1, 700, 600, 10, 100, projectile_group,
                         30, 4, 2)

    def update(self):
        # angle calculation
        self.angle = self.rot_compute(self.rect.center[0] - pygame.mouse.get_pos()[0],
                                      self.rect.center[1] - pygame.mouse.get_pos()[1])

        # key/mouse pressing
        #   wsad
        self.velocity += check_wsad()
        #   mouse
        mouse = pygame.mouse.get_pressed(num_buttons=5)
        if mouse[0]:
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
