import pygame
from ship import Ship
from screensetup import ScreenSetup
import numpy as np
import random
from projectile import Projectile
from pygame.sprite import Group


class Enemy(Ship):
    def __init__(self, start: np.ndarray, history_length: int, picture_path: str, max_velocity: int,
                 velocity_coefficient: float, hp: int, dmg: int, fire_rate: float, proj_dmg: int,
                 projectile_group: Group, overheat: int, cooling: float, explosion_size: int):

        super().__init__(picture_path, start, max_velocity, velocity_coefficient, hp, dmg, fire_rate, proj_dmg,
                         projectile_group, overheat, cooling, explosion_size)
        self.player_position_history = []  # Historie pozic hráče
        self.history_length = history_length

    def add_player_position_to_history(self, position):
        # Udržet historii na maximální délce
        if len(self.player_position_history) > self.history_length:
            self.player_position_history = self.player_position_history[-self.history_length:]

    def follow_movement(self, position):
        self.player_position_history.append(position)
    def random_movement(self, position):
        if self.rect.center[0] > position[0]:
            self.rect.center[0] -= self.velocity
        if self.rect.center[0] < position[0]:
            self.rect.center[0] += self.velocity
        if self.rect.center[1] > position[1]:
            self.rect.center[1] -= self.velocity
        if self.rect.center[1] < position[1]:
            self.rect.center[1] += self.velocity

        if self.rect.center[0] == position[0] + 20:
            self.velocity[0] = 0
        if self.rect.center[0] == position[0] - 20:
            self.velocity[0] = 0
        if self.rect.center[1] == position[1] + 20:
            self.velocity[1] = 0
        if self.rect.center[1] == position[1] - 20:
            self.velocity[1] = 0


    def update(self):
        # Získat nejnovější historickou pozici hráče
        if self.player_position_history:
            latest_player_pos = self.player_position_history[-1]

            # Vypočítat směr k nejnovější historické pozici hráče
            direction = np.array([latest_player_pos[0] - self.rect.center[0],
                                  latest_player_pos[1] - self.rect.center[1]])

            # Normalizovat směr, aby měl délku 1
            norm_direction = direction / np.linalg.norm(direction)

            # Přidat normalizovaný směr k rychlosti Enemy
            self.velocity[0] += norm_direction[0] * 2.2
            self.velocity[1] += norm_direction[1] * 2.2



            # Otáčení enemy k lodi
            self.angle = self.rot_compute(self.rect.center[0] - latest_player_pos[0],
                                          self.rect.center[1] - latest_player_pos[1])

        super().update()
