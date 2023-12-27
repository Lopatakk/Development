import random
from screensetup import ScreenSetup
import time
from enemies.zarovka import Zarovka
from enemies.tank import Tank
import numpy as np
from pygame.sprite import Group
from enemies.sniper import Sniper
from pygame.sprite import Sprite
import pygame
from enemies.stealer import Stealer
time_at_the_beginning = time.time()


class EnemySpawner(pygame.sprite.Sprite):
    def __init__(self, enemy_group: Group, enemy_type: str, spawn_interval, player: Sprite, shot_group: Group = None,
                 item_group: Group = None):
        super().__init__()
        self.enemy_group = enemy_group
        self.spawn_interval = spawn_interval
        self.screen_width = ScreenSetup.width
        self.screen_height = ScreenSetup.height
        self.enemy_type = enemy_type
        self.last_spawn_time = 0
        self.shot_group = shot_group
        self.player = player
        self.time_alive = 0
        self.scaling = 0
        self.item_group = item_group

        self.image = pygame.image.load("assets/images/spawner_lol.png")
        self.rect = self.image.get_rect()
        self.rect.center = [-70, -70]

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
        self.scaling = 1 + self.time_alive / 500
        start_time = time.time()
        elapsed_time = self.time_alive - self.last_spawn_time

        if self.enemy_type == "zarovka":
            if elapsed_time >= self.spawn_interval/self.scaling:
                # Spawnování nové nepřátelské lodě mimo obrazovku
                start = self.spawn_outside_screen()
                enemy = Zarovka(start, self.player)
                self.enemy_group.add(enemy)
                # Aktualizovat čas od posledního spawnu
                end_time = time.time()
                self.last_spawn_time = self.time_alive - (end_time - start_time)

        elif self.enemy_type == "tank":
            if elapsed_time >= self.spawn_interval/self.scaling:
                # Spawnování nové nepřátelské lodě mimo obrazovku
                start = self.spawn_outside_screen()
                enemy = Tank(start, self.shot_group, self.player)
                self.enemy_group.add(enemy)
                # Aktualizovat čas od posledního spawnu
                end_time = time.time()
                self.last_spawn_time = self.time_alive - (end_time - start_time)

        elif self.enemy_type == "sniper":
            if elapsed_time >= self.spawn_interval/self.scaling:
                # Spawnování nové nepřátelské lodě mimo obrazovku
                start = self.spawn_outside_screen()
                enemy = Sniper(start, self.shot_group, self.player)
                self.enemy_group.add(enemy)
                # Aktualizovat čas od posledního spawnu
                end_time = time.time()
                self.last_spawn_time = self.time_alive - (end_time - start_time)

        elif self.enemy_type == "stealer":
            for thing in self.item_group:
                if thing.time_alive >= 3 and not thing.has_thief:
                    start = self.spawn_outside_screen()
                    enemy = Stealer(start, self.player, thing)
                    self.enemy_group.add(enemy)
                    thing.has_thief = True
