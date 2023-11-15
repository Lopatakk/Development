from enemy import Enemy
import numpy as np


class Zarovka(Enemy):
    def __init__(self, start: np.ndarray):
        super().__init__(start, 5, "assets/images/zarovka.png", 37, 0.1, 100, 100, 0.1, 0, None)

    def update(self):

        super().update()
