import pygame
from ship import Ship
from screensetup import ScreenSetup
import numpy as np
class Zarovka(Ship):
    def __init__(self):
        super().__init__("vlod.png", ScreenSetup.width / 20, ScreenSetup.height / 20)
        self.vel = 0.09  # Nastavte rychlost "Zarovky" dle potřeby
        self.player_position = [0,0]
        self.velocity_coefficient = 0.052

    def update(self):
        # Vypočítat směr k "player_ship"
        direction = np.array([self.player_position[0] - self.pos[0], self.player_position[1] - self.pos[1]])
        if direction[0] > 0:
            self.velocity[0]+=1
        if direction[0] < 0:
            self.velocity[0]+=-1
        if direction[1] > 0:
            self.velocity[1]+=1
        if direction[1] < 0:
            self.velocity[1]+=-1
        # Nastavit novou pozici "Zarovky" tak, aby následovala "player_ship" s rychlostí self.vel
        super().update()