import pygame
import numpy as np
from screensetup import ScreenSetup
from ship import Ship


class PlayerShip(Ship):
    def __init__(self):
        super().__init__("vlod.png", ScreenSetup.width / 2, ScreenSetup.height / 2)

    def update(self):
        # angle calculation
        self.angle = self.rot_compute(self.rect.center[0] - pygame.mouse.get_pos()[0], self.rect.center[1] - pygame.mouse.get_pos()[1])
        super().update()
