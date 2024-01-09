import pygame
from projectile import Projectile
import numpy as np
from screensetup import ScreenSetup


class Blast(Projectile):
    def __init__(self, ship):
        super().__init__(ship)
        self.sound.stop()
        self.type = "blast"

        self.image = pygame.image.load("assets/images/blast.png")
        self.image = pygame.transform.scale_by(self.image, ScreenSetup.width / 1920)
        self.image = pygame.Surface.convert_alpha(self.image)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.pos = np.array([ship.rect.centerx - 1/1.9 * ship.height * np.sin(np.deg2rad(ship.angle)),
                             ship.rect.centery - 1/1.9 * ship.height * np.cos(np.deg2rad(ship.angle))])
        self.rect.center = self.pos

        self.velocity = 25

        self.recoil = 40
        ship.velocity += self.recoil * np.array([np.sin(np.deg2rad(self.angle)), np.cos(np.deg2rad(self.angle))])

        self.dmg = 100000

        self.sound = pygame.mixer.Sound("assets/sounds/blast_1.mp3")  # Load sound file
        self.sound.set_volume(0.3)
        pygame.mixer.find_channel(True).play(self.sound)

    def update(self):
        super().update()
        if self.pos[0] > ScreenSetup.width or self.pos[0] < 0 or self.pos[1] > ScreenSetup.height or self.pos[1] < 0:
            self.kill()

    def kill(self):
        super().kill()
        self.mask = None
