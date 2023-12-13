from enemy import Enemy
import numpy as np
import pygame


class Zarovka(Enemy):
    def __init__(self, start, clock, player):
        super().__init__(start, "assets/images/zarovka_new.png", 500, 600, 2, 41,
                         0.1, 0, 1, 0, 1, None,
                         clock, player)
        self.image_non_rot = pygame.transform.scale(self.image_non_rot, (120, 120))

    def update(self):
        self.follow_movement(5)
        super().update()
