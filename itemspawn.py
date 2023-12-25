import pygame
from screensetup import ScreenSetup
from medkit import Medkit
import random
import numpy as np
from pygame.sprite import Group
from pygame.sprite import Sprite


class ItemSpawner(pygame.sprite.Sprite):
    def __init__(self, item_group: Group, item: str, spawn_interval: int, player: Sprite):
        super().__init__()
        self.item_group = item_group
        self.spawn_interval = spawn_interval
        self.item = item
        self.player = player
        self.time_alive = 0
        self.last_spawn_time = 0

        self.image = pygame.image.load("assets/images/spawner_lol.png")
        self.rect = self.image.get_rect()
        self.rect.center = [-70, -70]

    def update(self):
        elapsed_time = self.time_alive - self.last_spawn_time
        match self.item:
            case "medkit":
                if elapsed_time >= self.spawn_interval:
                    medkit = Medkit(self.spawn_pos())
                    self.item_group.add(medkit)
                    self.last_spawn_time = self.time_alive

    @classmethod
    def spawn_pos(cls):
        side = random.choice(["t", "b", "l", "r"])
        # top
        if side == "t":
            return np.array([random.randint(0, ScreenSetup.width), random.randint(0, int(1/5*ScreenSetup.height))])
        # bottom
        elif side == "b":
            return np.array([random.randint(0, ScreenSetup.width), random.randint(int(4/5*ScreenSetup.height), ScreenSetup.height)])
        # left
        elif side == "l":
            return np.array([random.randint(0, int(1/6*ScreenSetup.width)), random.randint(0, ScreenSetup.height)])
        # right
        else:
            return np.array([random.randint(int(5/6*ScreenSetup.width), ScreenSetup.width), random.randint(0, ScreenSetup.height)])
