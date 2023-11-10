
import pygame
from zarovka import Zarovka
import random
from screensetup import ScreenSetup
import time
class EnemySpawner():
    def __init__(self, enemy_group, enemy_type, spawn_interval):
        self.enemy_group = enemy_group
        self.spawn_interval = spawn_interval  # Interval spawnování v sekundách
        self.screen_width = ScreenSetup.width
        self.screen_height = ScreenSetup.height
        self.time_since_last_spawn = 0
        self.image_path = f"{enemy_type}.png"  # Přidáváme příponu .png k názvu obrázku
        self.last_spawn_time = time.time()

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

        if elapsed_time >= self.spawn_interval:
            # Spawnování nové nepřátelské lodě mimo obrazovku
            start_x, start_y = self.spawn_outside_screen()
            enemy = Zarovka(start_x, start_y)
            self.enemy_group.add(enemy)
            enemy.add_player_position_to_history(player_pos)

            # Aktualizovat čas od posledního spawnu
            self.last_spawn_time = time.time()

