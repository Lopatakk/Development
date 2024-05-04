import random
from gamesetup import GameSetup
import time
from enemies.zarovka import Zarovka
from enemies.tank import Tank
import numpy as np
from pygame.sprite import Group
from enemies.sniper import Sniper
from pygame.sprite import Sprite
import pygame
from enemies.stealer import Stealer
from enemies.minigame.minizarovka import MiniZarovka
time_at_the_beginning = time.time()


class EnemySpawner(pygame.sprite.Sprite):
    def __init__(self, enemy_group: Group, enemy_type: str, spawn_interval, player: Sprite, projectile_group: Group = None,
                 item_group: Group = None):
        super().__init__()
        self.enemy_group = enemy_group
        self.spawn_interval = spawn_interval
        self.screen_width = GameSetup.width
        self.screen_height = GameSetup.height
        self.enemy_type = enemy_type
        if self.enemy_type == "minizarovka":
            self.last_spawn_time = -1
        else:
            self.last_spawn_time = -5
        self.projectile_group = projectile_group
        self.player = player
        self.time_alive = 0
        self.scaling = 0
        self.item_group = item_group

        self.image = pygame.image.load("assets/images/spawner_lol.png")
        self.warning_icon = pygame.image.load("assets/images/cockpit/warning.png")
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

    def spawn_outside_mini_screen(self):
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            return np.array([random.randint(515, GameSetup.width - 515), 285])
        elif side == "bottom":
            return np.array([random.randint(515, GameSetup.width - 515), GameSetup.height - 305])
        elif side == "left":
            return np.array([515, random.randint(285, GameSetup.height - 305)])
        elif side == "right":
            return np.array([GameSetup.width - 515, random.randint(285, GameSetup.height - 305)])

    def update(self):
        self.scaling = 1 + self.time_alive / 500

        start_time = time.time()
        elapsed_time = self.time_alive - self.last_spawn_time

        if self.enemy_type == "zarovka":
            ship = Zarovka
            start_pos = self.spawn_outside_screen()
            self.spawn_ship(ship, start_pos, start_time, elapsed_time)
        elif self.enemy_type == "sniper":
            ship = Sniper
            start_pos = self.spawn_outside_screen()
            self.spawn_ship(ship, start_pos, start_time, elapsed_time, self.projectile_group)
        elif self.enemy_type == "tank":
            ship = Tank
            start_pos = self.spawn_outside_screen()
            self.spawn_ship(ship, start_pos, start_time, elapsed_time, self.projectile_group)
        elif self.enemy_type == "stealer":
            for thing in self.item_group:
                if thing.type == "medkit":
                    if thing.time_alive >= 3 and not thing.has_thief:
                        start_pos = self.spawn_outside_screen()
                        enemy = Stealer(start_pos, self.player, thing)
                        self.enemy_group.add(enemy)
                        thing.has_thief = True
        elif self.enemy_type == "minizarovka":
            ship = MiniZarovka
            start_pos = self.spawn_outside_mini_screen()
            self.spawn_ship(ship, start_pos, start_time, elapsed_time)

    def spawn_ship(self, ship, start_pos, start_time, elapsed_time, projectile_group=None):
        if elapsed_time >= self.spawn_interval / self.scaling:
            # Spawnování nové nepřátelské lodě mimo obrazovku
            if ship == Zarovka or ship == MiniZarovka:
                enemy = ship(start_pos, self.player)
            else:
                enemy = ship(start_pos, projectile_group, self.player)
            self.enemy_group.add(enemy)
            # Aktualizovat čas od posledního spawnu
            end_time = time.time()
            self.last_spawn_time = self.time_alive - (end_time - start_time)

    def find_start_position(self):
        if self.enemy_type == "minizarovka":
            self.last_spawn_time = 1
            start = self.spawn_outside_mini_screen()
        else:
            self.last_spawn_time = -5
            start = self.spawn_outside_screen()
        return start

