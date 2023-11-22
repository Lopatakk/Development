from enemy import Enemy
import numpy as np
import pygame


class Zarovka(Enemy):
    def __init__(self, start: np.ndarray):
        super().__init__(start, 5, "assets/images/zarovka_new.png", 39, 0.1, 600, 600, 1, 0, 1, 1, None)
        self.image_non_rot = pygame.transform.scale(self.image_non_rot, (120, 120))

    def update(self):
        super().update()
