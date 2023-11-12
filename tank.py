from enemy import Enemy
import pygame
import numpy as np


class Tank(Enemy):
    def __init__(self, start: np.ndarray, shot_group):
        super().__init__(start, 8, "tank", 30, 0.1, 4500, 100)

        self.last_function_call = pygame.time.get_ticks()  # Uložení času posledního volání funkce v milisekundách
        self.function_interval = 2000  # Interval v milisekundách
        self.shot_group = shot_group

    def update(self):
        current_time = pygame.time.get_ticks()

        # fire rate
        if current_time - self.last_function_call >= self.function_interval:
            enemy_projectile = self.shoot()
            self.shot_group.add(enemy_projectile)
            self.last_function_call = current_time  # Aktualizace času posledního volání funkce
            return enemy_projectile

        super().update()
