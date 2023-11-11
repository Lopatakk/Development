from enemy import Enemy

class Tank(Enemy):
    def __init__(self, start_x, start_y):
        super().__init__(start_x, start_y, 5, "tank", 30, 0.1, 4500, 100)


    def update(self):

        super().update()