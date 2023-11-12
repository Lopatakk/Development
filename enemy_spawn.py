
import pygame
from enemy import Enemy
import random
from screensetup import ScreenSetup
import time
from zarovka import Zarovka
from tank import Tank
class EnemySpawner():
    def __init__(self, group, enemy_type, spawn_interval, shot_group):
        self.enemy_group = group
        self.spawn_interval = spawn_interval  # Interval spawnování v sekundách
        self.screen_width = ScreenSetup.width
        self.screen_height = ScreenSetup.height
        self.time_since_last_spawn = 0
        self.enemy_type = enemy_type
        self.last_spawn_time = time.time()
        self.shot_group = shot_group


    def spawn_outside_screen(self):
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            return random.randint(0, self.screen_width), -50
        elif side == "bottom":
            return random.randint(0, self.screen_width), self.screen_height + 50
        elif side == "left":
            return -50, random.randint(0, self.screen_height)
        elif side == "right":
            return self.screen_width + 50, random.randint(0, self.screen_height)

    def update(self, player_pos):
        current_time = time.time()
        elapsed_time = current_time - self.last_spawn_time
        if self.enemy_type == "zarovka":
            if elapsed_time >= self.spawn_interval:
                # Spawnování nové nepřátelské lodě mimo obrazovku
                start_x, start_y = self.spawn_outside_screen()
                enemy = Zarovka(start_x, start_y)
                self.enemy_group.add(enemy)
                enemy.add_player_position_to_history(player_pos)
                # Aktualizovat čas od posledního spawnu
                self.last_spawn_time = time.time()

        if self.enemy_type == "tank":
            if elapsed_time >= self.spawn_interval:
                # Spawnování nové nepřátelské lodě mimo obrazovku
                start_x, start_y = self.spawn_outside_screen()
                enemy = Tank(start_x, start_y, self.shot_group)
                self.enemy_group.add(enemy)
                enemy.add_player_position_to_history(player_pos)
                # Aktualizovat čas od posledního spawnu
                self.last_spawn_time = time.time()