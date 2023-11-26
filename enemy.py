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
                 projectile_group: Group, overheat: int, cooling: float, explosion_size: int, player):

        super().__init__(picture_path, start, max_velocity, velocity_coefficient, hp, dmg, fire_rate, proj_dmg,
                         projectile_group, overheat, cooling, explosion_size)
        self.player = player
        self.tolerance = None
        self.player_position_history = []  # Historie pozic hráče
        self.history_length = history_length    # Sets length of player_position_history
                                                # aka how many position of player we save

    def follow_movement(self):
        # Udržet historii na maximální délce
        self.player_position_history.append(self.player.pos)
        if len(self.player_position_history) > self.history_length:
            self.player_position_history.pop(0)

        if self.player_position_history:
            oldest_player_pos = self.player_position_history[0]

            # Vypočítat směr k nejstarší historické pozici hráče
            direction = np.array([oldest_player_pos[0] - self.rect.center[0],
                                  oldest_player_pos[1] - self.rect.center[1]])

            # Normalizovat směr, aby měl délku 1
            norm_direction = direction / np.linalg.norm(direction)

            # Přidat normalizovaný směr k rychlosti Enemy
            self.velocity[0] += norm_direction[0] * 2.2
            self.velocity[1] += norm_direction[1] * 2.2

            # Otáčení enemy k lodi
            self.angle = self.rot_compute(self.rect.center[0] - oldest_player_pos[0],
                                          self.rect.center[1] - oldest_player_pos[1])

    def follow_movement_with_offset(self, offset, tolerance):
        self.offset = offset
        self.tolerance = tolerance
        # Náhodný pohyb na ose X
        self.velocity[0] += np.random.uniform(-0.1, 0.1)

        # Náhodný pohyb na ose Y
        self.velocity[1] += np.random.uniform(-0.1, 0.1)

        # Normalizovat rychlost, aby nedošlo k nekontrolovanému pohybu
        norm_velocity = np.linalg.norm(self.velocity)
        if norm_velocity > self.max_velocity:
            self.velocity = self.velocity / norm_velocity * self.max_velocity

        # Vypočítat směr k hráči
        direction = np.array([self.player.pos[0] - self.pos[0], self.player.pos[1] - self.pos[1]])

        # Normalizovat směr, aby měl délku 1
        norm_direction = direction / np.linalg.norm(direction)

        # Nastavit délku směru na pevnou vzdálenost (offset)
        target_distance = self.offset
        scaled_direction = norm_direction * target_distance

        # Vypočítat novou pozici cíle
        target_position = np.array([self.pos[0] + scaled_direction[0], self.pos[1] + scaled_direction[1]])

        # Vypočítat směr k novému cíli
        new_direction = np.array([target_position[0] - self.pos[0], target_position[1] - self.pos[1]])

        # Zastavit lod, pokud je vzdálenost od cíle menší než offset
        distance = np.linalg.norm(direction)
        if distance - self.tolerance <= self.offset:
            self.velocity[0] = -self.max_velocity
            self.velocity[1] = -self.max_velocity
        else:
            # Přidat normalizovaný směr k rychlosti Enemy, pokud není vzdálenost menší než offset
            self.velocity[0] += new_direction[0] * 2.2
            self.velocity[1] += new_direction[1] * 2.2

        # Ošetřit okraje obrazovky
        self.pos[0] = np.clip(self.pos[0], 0, ScreenSetup.width)
        self.pos[1] = np.clip(self.pos[1], 0, ScreenSetup.height)

        # Otáčení enemy k lodi
        self.angle = self.rot_compute(self.rect.center[0] - self.player.pos[0],
                                      self.rect.center[1] - self.player.pos[1])

    def update(self):
        super().update()
