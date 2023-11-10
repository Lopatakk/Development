import pygame
import random
import time
from screensetup import ScreenSetup
from zarovka import Zarovka

class EnemySpawner():
    def __init__(self, enemy_group, spawn_interval):
        self.enemy_group = enemy_group
        self.spawn_interval = spawn_interval
        self.last_spawn_time = time.time()

    def update(self, player_pos):
        current_time = time.time()
        elapsed_time = current_time - self.last_spawn_time

        if elapsed_time >= self.spawn_interval:
            self.spawn_enemy(player_pos)
            self.last_spawn_time = current_time

    def spawn_enemy(self, player_pos):
        start_x = random.choice([-50, ScreenSetup.width + 50])
        start_y = random.choice([-50, ScreenSetup.height + 50])
        zarovka = Zarovka(start_x, start_y)
        self.enemy_group.add(zarovka)
        zarovka.add_player_position_to_history(player_pos)


