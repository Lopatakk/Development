import pygame
from ship import Ship
from screensetup import ScreenSetup
import numpy as np
import random
from projectile import Projectile
from pygame.sprite import Group


class Enemy(Ship):
    def __init__(self, start: np.ndarray, history_length: int, picture_path: str, clock, max_velocity: int,
                 velocity_coefficient: float, hp: int, dmg: int, fire_rate: float, proj_dmg: int,
                 projectile_group: Group, overheat: int, cooling: float, explosion_size: int, player):

        super().__init__(picture_path, clock, start, max_velocity, velocity_coefficient, hp, dmg, fire_rate, proj_dmg,
                         projectile_group, overheat, cooling, explosion_size)
        self.player = player
        self.tolerance = None
        self.player_position_history = []  # Historie pozic hráče
        self.history_length = history_length    # Sets length of player_position_history
                                                # aka how many position of player we save
        self.rot_freq = 0.3
        self.omega = 2 * np.pi * self.rot_freq
        self.offset = 0

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

    def follow_movement_with_offset(self, offset):
        self.offset = offset
        # Vypočítat směr k hráči
        direction = np.array([self.player.pos[0] - self.pos[0], self.player.pos[1] - self.pos[1]])
        # Normalizovat směr, aby měl délku 1
        norm_direction = direction / np.linalg.norm(direction)
        # vypocet vzdalenosti
        player_distance = (direction[0]**2 + direction[1]**2) ** (1/2)

        # kdyz je bliz nez ma
        if player_distance <= self.offset:
            self.velocity[0] += -norm_direction[0] * 2.2
            self.velocity[1] += -norm_direction[1] * 2.2
        else:
            # kdyz je dal nez muze
            self.velocity[0] += norm_direction[0] * 2.2
            self.velocity[1] += norm_direction[1] * 2.2

        # Ošetřit okraje obrazovky
        self.pos[0] = np.clip(self.pos[0], 0, ScreenSetup.width)
        self.pos[1] = np.clip(self.pos[1], 0, ScreenSetup.height)

        # Otáčení enemy k lodi
        self.angle = self.rot_compute(self.rect.center[0] - self.player.pos[0],
                                      self.rect.center[1] - self.player.pos[1])

    def angle_speed(self, rot_direction):
        direction = np.array([self.player.pos[0] - self.pos[0], self.player.pos[1] - self.pos[1]])
        tang_vector = np.array([direction[1]*rot_direction, direction[0]*rot_direction*(-1)])
        hypotenuse = (tang_vector[0]**2 + tang_vector[1]**2)**(1/2)
        norm_vector = tang_vector / hypotenuse
        rot_vector = norm_vector * 5
        rot_vector = np.array([int(rot_vector[0]), int(rot_vector[1])])
        self.velocity += rot_vector

    def update(self):
        super().update()
