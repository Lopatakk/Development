import pygame
import random
from gamesetup import GameSetup


class ScrapMetal(pygame.sprite.Sprite):
    def __init__(self, pos, velocity, velocity_coefficient):
        super().__init__()
        self.pos = tuple(pos)
        self.time_alive = 0
        self.type = "scrap_metal"
        self.velocity = velocity
        self.velocity_coefficient = velocity_coefficient
        self.angle = 0
        self.angle_increment = random.uniform(-10, 10)

        if random.random() < 0.5:
            self.unscaled_image = pygame.image.load(f"assets/images/scrap_metal0.png").convert_alpha()
        else:
            self.unscaled_image = pygame.image.load(f"assets/images/scrap_metal1.png").convert_alpha()

        self.image_non_rot = pygame.transform.scale(self.unscaled_image, (64, 64))
        self.image_non_rot = pygame.transform.scale_by(self.image_non_rot, GameSetup.width / 1920)
        self.image_non_rot = pygame.Surface.convert_alpha(self.image_non_rot)
        self.image_orig = self.image_non_rot
        self.image = self.image_orig
        self.rect_non_rot = self.image.get_rect()
        self.rect = self.rect_non_rot
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = pos

        self.sound = pygame.mixer.Sound("assets/sounds/scrap_metal_collect.mp3")  # Load sound file
        self.sound.set_volume(0.2 * GameSetup.effects_volume)

    def update(self):
        # moving after the destruction of the ship
        self.pos = (self.pos[0] + self.velocity[0] * self.velocity_coefficient / 3, self.pos[1] + self.velocity[1] * self.velocity_coefficient / 3)

        self.rect_non_rot.x = self.pos[0]
        self.rect_non_rot.y = self.pos[1]

        # rotation
        self.angle += self.angle_increment

        self.image = pygame.transform.rotate(self.image_non_rot, self.angle)
        self.rect = self.image.get_rect(center=self.rect_non_rot.center)
        self.mask = pygame.mask.from_surface(self.image)

        super().update()
