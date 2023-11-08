import pygame
from ship import Ship
from screensetup import ScreenSetup
import numpy as np
import random
class Zarovka(Ship):
    def __init__(self, start_x,start_y):

        super().__init__("zarovka.png", start_x, start_y,35,1000,0.1)
        self.player_position = [0,0]
        self.dmg = 100


    def update(self):
        # Vypočítat směr k "player_ship"
        direction = np.array([self.player_position[0] - self.pos[0], self.player_position[1] - self.pos[1]])
        if direction[0] > 0:
            self.velocity[0]+=2.2
        if direction[0] < 0:
            self.velocity[0]+=-2.2
        if direction[1] > 0:
            self.velocity[1]+=2.2
        if direction[1] < 0:
            self.velocity[1]+=-2.2
        #if self.hp <= 0:
            #self.mask = None
            #self.kill()
        # Otaceni zarovky k lodi
        self.angle = self.rot_compute(self.rect.center[0] - self.player_position[0],
                                      self.rect.center[1] - self.player_position[1])

        super().update()

