from enemy import Enemy
import numpy as np


class Zarovka(Enemy):
    def __init__(self, start: np.ndarray):
        super().__init__(start, 5, "zarovka", 37, 0.1, 1000, 100)

    def update(self):

        super().update()
