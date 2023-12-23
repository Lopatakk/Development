import pygame
from projectile import Projectile
import numpy as np


class Blast(Projectile):
    def __init__(self, ship):
        super().__init__(ship)
        self.sound.stop()

        self.image = pygame.image.load("assets/images/blast.png")
        self.image = pygame.Surface.convert(self.image)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.pos = np.array([ship.rect.centerx - 1/1.9 * ship.height * np.sin(np.deg2rad(ship.angle)),
                             ship.rect.centery - 1/1.9 * ship.height * np.cos(np.deg2rad(ship.angle))])
        self.rect.center = self.pos

        self.velocity = 25

        self.dmg = 100000

        self.sound = pygame.mixer.Sound("assets/sounds/blast_1.mp3")  # Load sound file
        self.sound.set_volume(0.3)
        pygame.mixer.find_channel(True).play(self.sound)

        # recoil
        ship.velocity += 25 * np.array([np.sin(np.deg2rad(self.angle)), np.cos(np.deg2rad(self.angle))])

    def update(self):
        super().update()
