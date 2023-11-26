import pygame
from enemy import Enemy
import random
from screensetup import ScreenSetup
import time
from zarovka import Zarovka
from tank import Tank
import numpy as np
from pygame.sprite import Group
from sniper import Sniper

time_at_the_beginning = time.time()


class EnemySpawner:
    def __init__(self, enemy_group: Group, enemy_type: str, spawn_interval, clock, shot_group: Group, player):
        self.enemy_group = enemy_group
        self.spawn_interval = spawn_interval
        self.screen_width = ScreenSetup.width
        self.screen_height = ScreenSetup.height
        self.enemy_type = enemy_type
        self.last_spawn_time = 0
        self.shot_group = shot_group
        self.player = player
        self.clock = clock
        self.time_working = 0

    def spawn_outside_screen(self):
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            return np.array([random.randint(0, self.screen_width), -50])
        elif side == "bottom":
            return np.array([random.randint(0, self.screen_width), self.screen_height + 50])
        elif side == "left":
            return np.array([-50, random.randint(0, self.screen_height)])
        elif side == "right":
            return np.array([self.screen_width + 50, random.randint(0, self.screen_height)])

    def update(self):
        self.time_working += self.clock.get_time()
        start_time = time.time() * 1000  # to miliseconds
        elapsed_time = self.time_working - self.last_spawn_time
        if self.enemy_type == "zarovka":
            if elapsed_time >= self.spawn_interval:
                # Spawnování nové nepřátelské lodě mimo obrazovku
                start = self.spawn_outside_screen()
                enemy = Zarovka(start, self.clock, self.player)
                self.enemy_group.add(enemy)
                # Aktualizovat čas od posledního spawnu
                end_time = time.time() * 1000  # to miliseconds
                self.last_spawn_time = self.time_working - (end_time - start_time)

        elif self.enemy_type == "tank":
            if elapsed_time >= self.spawn_interval:
                # Spawnování nové nepřátelské lodě mimo obrazovku
                start = self.spawn_outside_screen()
                enemy = Tank(start, self.clock, self.shot_group, self.player)
                self.enemy_group.add(enemy)
                # Aktualizovat čas od posledního spawnu
                end_time = time.time() * 1000  # to miliseconds
                self.last_spawn_time = self.time_working - (end_time - start_time)

        elif self.enemy_type == "sniper":
            if elapsed_time >= self.spawn_interval:
                # Spawnování nové nepřátelské lodě mimo obrazovku
                start = self.spawn_outside_screen()
                enemy = Sniper(start, self.clock, self.shot_group, self.player)
                self.enemy_group.add(enemy)
                # Aktualizovat čas od posledního spawnu
                end_time = time.time() * 1000  # to miliseconds
                self.last_spawn_time = self.time_working - (end_time - start_time)
