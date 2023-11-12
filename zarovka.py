from enemy import Enemy

class Zarovka(Enemy):
    def __init__(self, start_x, start_y):
        super().__init__(start_x, start_y, 5, "zarovka", 37, 0.1, 1000, 100)

    def update(self):

        super().update()