import pygame
from ship import Ship
from screensetup import ScreenSetup
import numpy as np
import random

class Zarovka(Ship):
    def __init__(self, start_x, start_y, history_length=5):
        super().__init__("zarovka.png", start_x, start_y, 35, 1000, 0.1)
        self.player_position_history = []  # Historie pozic hráče
        self.dmg = 100
        self.history_length = history_length

    def add_player_position_to_history(self, position):
        self.player_position_history.append(position)
        # Udržet historii na maximální délce
        if len(self.player_position_history) > self.history_length:
            self.player_position_history = self.player_position_history[-self.history_length:]

    def update(self):
        # Získat nejnovější historickou pozici hráče
        if self.player_position_history:
            latest_player_pos = self.player_position_history[-1]

            # Vypočítat směr k nejnovější historické pozici hráče
            direction = np.array([latest_player_pos[0] - self.rect.center[0], latest_player_pos[1] - self.rect.center[1]])

            # Normalizovat směr, aby měl délku 1
            norm_direction = direction / np.linalg.norm(direction)

            # Přidat normalizovaný směr k rychlosti Zarovky
            self.velocity[0] += norm_direction[0] * 2.2
            self.velocity[1] += norm_direction[1] * 2.2

            # Otáčení zarovky k lodi
            self.angle = self.rot_compute(self.rect.center[0] - latest_player_pos[0],
                                          self.rect.center[1] - latest_player_pos[1])

        super().update()


