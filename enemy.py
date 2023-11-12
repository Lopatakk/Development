import pygame
from ship import Ship
from screensetup import ScreenSetup
import numpy as np
import random
from projectile import Projectile


class Enemy(Ship):
    def __init__(self, start: np.ndarray, history_length: int, enemy_model: str, max_velocity: int, velocity_coefficient: float, hp: int, dmg, fire_rate):
        super().__init__(f"{enemy_model}.png", start, max_velocity, velocity_coefficient, hp, dmg, fire_rate)
        self.player_position_history = []  # Historie pozic hráče
        self.history_length = history_length

    def add_player_position_to_history(self, position):
        self.player_position_history.append(position)
        # Udržet historii na maximální délce
        if len(self.player_position_history) > self.history_length:
            self.player_position_history = self.player_position_history[-self.history_length:]

    def shoot(self):
        projectile = Projectile(self)
        return projectile

    def update(self):
        # Získat nejnovější historickou pozici hráče
        if self.player_position_history:
            latest_player_pos = self.player_position_history[-1]

            # Vypočítat směr k nejnovější historické pozici hráče
            direction = np.array([latest_player_pos[0] - self.rect.center[0], latest_player_pos[1] - self.rect.center[1]])

            # Normalizovat směr, aby měl délku 1
            norm_direction = direction / np.linalg.norm(direction)

            # Přidat normalizovaný směr k rychlosti Enemy
            self.velocity[0] += norm_direction[0] * 2.2
            self.velocity[1] += norm_direction[1] * 2.2

            # Otáčení enemy k lodi
            self.angle = self.rot_compute(self.rect.center[0] - latest_player_pos[0],
                                          self.rect.center[1] - latest_player_pos[1])

        super().update()
