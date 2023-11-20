from enemy import Enemy
import numpy as np


class Zarovka(Enemy):
    def __init__(self, start: np.ndarray):
        super().__init__(start, 5, "assets/images/zarovka.png", 39, 0.1, 600, 600, 1, 0, 1, 1, None)

    def update(self):

        super().update()
