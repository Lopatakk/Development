import pygame
from ship import Ship
from gamesetup import GameSetup
import numpy as np
import random
from projectile import Projectile
from pygame.sprite import Sprite


class Enemy(Ship):
    def __init__(self, start: np.ndarray, image, img_scaling_coefficient, ani_amount_of_images,
                 ship_type, hp, dmg, explosion_size,
                 max_velocity, acceleration, velocity_coefficient, rot_velocity,
                 proj_dmg, fire_rate, cooling, overheat, offset, mini, projectile_group, player: Sprite):

        super().__init__(start, image, None, hp, acceleration, dmg, proj_dmg, fire_rate,
                         overheat, cooling, 0, img_scaling_coefficient, ani_amount_of_images,
                         ship_type, explosion_size, max_velocity, velocity_coefficient, mini,
                         projectile_group)

        self.player_position_history = []  # player pos history
        self.player = player
        self.rot_velocity = rot_velocity
        self.offset = offset
        self.oldest_player_pos = [0, 0]
        self.direction = np.array([self.oldest_player_pos[0] - self.pos[0], self.oldest_player_pos[1] - self.pos[1]])

    def follow_movement(self, history_length):
        # history_length sets length of player_position_history, aka how many position of player we save
        # Udržet historii na maximální délce
        self.player_position_history.append(self.player.pos) # stores positions of player
        if len(self.player_position_history) > history_length:
            self.oldest_player_pos = self.player_position_history.pop(0) # returns latest position of player and removes it from the list

        # Vypočítat směr k nejstarší historické pozici hráče
        self.direction = np.array([self.oldest_player_pos[0] - self.pos[0], self.oldest_player_pos[1] - self.pos[1]]) # vector pointing at player

        # Normalizovat směr, aby měl délku 1
        norm_direction = self.direction / np.linalg.norm(self.direction) # norm vector pointing towards player (his size = 1)

        # Přidat normalizovaný směr k rychlosti Enemy
        self.velocity[0] += norm_direction[0] * self.acceleration # updating positon through velocity with use of norm vector
        self.velocity[1] += norm_direction[1] * self.acceleration

        # Otáčení enemy k lodi
        self.angle = self.rot_compute(self.pos[0] - self.oldest_player_pos[0],
                                          self.pos[1] - self.oldest_player_pos[1])

    def follow_movement_with_offset(self):
        # Normalizovat směr, aby měl délku 1
        norm_direction = self.direction / np.linalg.norm(self.direction)
        # vypocet vzdalenosti
        player_distance = (self.direction[0]**2 + self.direction[1]**2) ** (1/2)

        # kdyz je bliz nez ma
        if player_distance <= self.offset:
            self.velocity[0] -= norm_direction[0] * self.acceleration
            self.velocity[1] -= norm_direction[1] * self.acceleration
        else:
            # kdyz je dal nez muze
            self.velocity[0] += norm_direction[0] * self.acceleration
            self.velocity[1] += norm_direction[1] * self.acceleration

        # Ošetřit okraje obrazovky
        self.pos[0] = np.clip(self.pos[0], 0, GameSetup.width)
        self.pos[1] = np.clip(self.pos[1], 0, GameSetup.height)

        # Otáčení enemy k lodi
        self.angle = self.rot_compute(self.rect.center[0] - self.player.pos[0],
                                      self.rect.center[1] - self.player.pos[1])

    def angle_speed(self, rot_direction):
        # nromála vektoru direction(tečna kružnice pohybu)
        normal_vector = np.array([self.direction[1]*rot_direction, self.direction[0]*rot_direction*(-1)])
        # přepona delty x a y
        hypotenuse = (normal_vector[0]**2 + normal_vector[1]**2)**(1/2)
        # normalovy vektor (vždy velikost rovna 1 => rika smer kterym se ma lod pohybovat)
        norm_vector = normal_vector / hypotenuse

        rot_vector = norm_vector * self.rot_velocity
        rot_vector = np.array([int(rot_vector[0]), int(rot_vector[1])])
        self.velocity += rot_vector

    def item_follow(self, item_pos):
        # normalovy vektor, ktery zajisti stejnou rychlost lodi ve smeru k cili
        norm_direction = self.direction / np.linalg.norm(self.direction)
        self.velocity[0] += norm_direction[0] * self.acceleration
        self.velocity[1] += norm_direction[1] * self.acceleration
        # otaceni modelu
        self.angle = self.rot_compute(self.pos[0] - item_pos[0],
                                      self.pos[1] - item_pos[1])

    def find_direction(self, target):
        self.direction = np.array([target[0] - self.pos[0], target[1] - self.pos[1]])

    def update(self):
        super().update()
