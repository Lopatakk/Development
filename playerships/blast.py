import pygame
from projectile import Projectile
import numpy as np
from gamesetup import GameSetup


class Blast(Projectile):
    def __init__(self, ship):
        super().__init__(ship)
        self.sound.stop()
        self.type = "blast"

        self.image = pygame.image.load("assets/animations/blast/blast1.png")
        self.image = pygame.transform.scale_by(self.image, GameSetup.width / 3840)
        self.image = pygame.Surface.convert_alpha(self.image)
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.pos = np.array([ship.rect.centerx - 1/1.9 * ship.height * np.sin(np.deg2rad(ship.angle)),
                             ship.rect.centery - 1/1.9 * ship.height * np.cos(np.deg2rad(ship.angle))])
        self.rect.center = self.pos

        self.velocity = 25

        self.recoil = 60
        ship.velocity += self.recoil * np.array([np.sin(np.deg2rad(self.angle)), np.cos(np.deg2rad(self.angle))])

        self.dmg = 100000

        self.sound = pygame.mixer.Sound("assets/sounds/blast_1.mp3")  # Load sound file
        self.sound.set_volume(0.3 * GameSetup.effects_volume)
        pygame.mixer.find_channel(False).play(self.sound)

        # flying animation setup
        self.image_orig = self.image
        self.animation_images = []
        for num in range(2, 4):
            img = pygame.image.load(f"assets/animations/blast/blast{num}.png")
            img = pygame.transform.scale_by(img, GameSetup.width / 3840)
            img = pygame.transform.rotate(img, self.angle)
            img = pygame.Surface.convert_alpha(img)
            self.animation_images.append(img)
        self.index = 0
        self.counter = 0
        self.animation_speed = 2

    def update(self):
        # flying animation
        if self.counter >= 0:
            self.counter += 1
        #   changing the picture
        if self.counter >= self.animation_speed and self.index < len(self.animation_images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.animation_images[self.index]
        #   end of the animation
        if self.index >= len(self.animation_images) - 1 and self.counter >= self.animation_speed:
            self.counter = 0
            self.index = 0
            self.image = self.image_orig

        super().update()
        if self.pos[0] > GameSetup.width or self.pos[0] < 0 or self.pos[1] > GameSetup.height or self.pos[1] < 0:
            self.kill()

    def kill(self):
        super().kill()
        self.mask = None
