import pygame
from ship import Ship
from screensetup import ScreenSetup
import numpy as np
import random
from projectile import Projectile
from pygame.sprite import Sprite


class Enemy(Ship):
    def __init__(self, start: np.ndarray, picture_path, hp, dmg, explosion_size, max_velocity, acceleration,
                 velocity_coefficient, rot_velocity, proj_dmg, fire_rate, cooling, overheat, offset, projectile_group,
                 player: Sprite):

        super().__init__(start, picture_path, hp, dmg, explosion_size, max_velocity, acceleration, velocity_coefficient,
                         proj_dmg, fire_rate, cooling, overheat, projectile_group)
        self.tolerance = None
        self.player_position_history = []  # Historie pozic hráče

        self.player = player
        self.rot_velocity = rot_velocity
        self.offset = offset

    def follow_movement(self, history_length):
        self.history_length = history_length    # Sets length of player_position_history
                                                # aka how many position of player we save
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
            self.velocity[0] += norm_direction[0] * self.acceleration
            self.velocity[1] += norm_direction[1] * self.acceleration

            # Otáčení enemy k lodi
            self.angle = self.rot_compute(self.rect.center[0] - oldest_player_pos[0],
                                          self.rect.center[1] - oldest_player_pos[1])

    def follow_movement_with_offset(self):
        # Vypočítat směr k hráči
        direction = np.array([self.player.pos[0] - self.pos[0], self.player.pos[1] - self.pos[1]])
        # Normalizovat směr, aby měl délku 1
        norm_direction = direction / np.linalg.norm(direction)
        # vypocet vzdalenosti
        player_distance = (direction[0]**2 + direction[1]**2) ** (1/2)

        # kdyz je bliz nez ma
        if player_distance <= self.offset:
            self.velocity[0] -= norm_direction[0] * self.acceleration
            self.velocity[1] -= norm_direction[1] * self.acceleration
        else:
            # kdyz je dal nez muze
            self.velocity[0] += norm_direction[0] * self.acceleration
            self.velocity[1] += norm_direction[1] * self.acceleration

        # Ošetřit okraje obrazovky
        self.pos[0] = np.clip(self.pos[0], 0, ScreenSetup.width)
        self.pos[1] = np.clip(self.pos[1], 0, ScreenSetup.height)

        # Otáčení enemy k lodi
        self.angle = self.rot_compute(self.rect.center[0] - self.player.pos[0],
                                      self.rect.center[1] - self.player.pos[1])

    def angle_speed(self, rot_direction):
        # delta x a delta y hrace a enemy
        direction = np.array([self.player.pos[0] - self.pos[0], self.player.pos[1] - self.pos[1]])
        # nromála vektoru direction(tečna kružnice pohybu)
        normal_vector = np.array([direction[1]*rot_direction, direction[0]*rot_direction*(-1)])
        # přepona delty x a y
        hypotenuse = (normal_vector[0]**2 + normal_vector[1]**2)**(1/2)
        # normalovy vektor (vždy velikost rovna 1 => rika smer kterym se ma lod pohybovat)
        norm_vector = normal_vector / hypotenuse

        rot_vector = norm_vector * self.rot_velocity
        rot_vector = np.array([int(rot_vector[0]), int(rot_vector[1])])
        self.velocity += rot_vector

    def update(self):
        super().update()
