import pygame
import random
from gamesetup import GameSetup


class ShipUpgrade(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, upgrade_type: str, upgradable: bool, velocity=0, velocity_coefficient=0):
        super().__init__()
        self.pos = pos
        self.velocity = velocity
        self.velocity_coefficient = velocity_coefficient
        self.angle = 0
        self.angle_increment = random.uniform(-5, 5)

        self.time_alive = 0
        self.type = "ship_upgrade"
        self.upgrade_type = upgrade_type
        self.upgradable = upgradable
        if upgradable:
            self.level = 0
        else:
            self.level = 1

        ship_parts = {'weapons',
                      'cooling',
                      'repair_module',
                      'shield',
                      'booster'}
        for module in ship_parts:
            if self.upgrade_type == module:
                if upgradable:
                    self.unscaled_image = pygame.image.load(f"assets/images/{module}_part.png").convert_alpha()
                else:
                    self.unscaled_image = pygame.image.load(f"assets/images/{module}0.png").convert_alpha()

        self.image_non_rot = pygame.transform.scale(self.unscaled_image, (128, 128))
        self.image_non_rot = pygame.transform.scale_by(self.image_non_rot, GameSetup.width / 1920)
        self.image_non_rot = pygame.Surface.convert_alpha(self.image_non_rot)
        self.image_orig = self.image_non_rot
        self.image = self.image_orig
        self.rect_non_rot = self.image.get_rect()
        self.rect = self.rect_non_rot
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = self.pos

        self.sound = pygame.mixer.Sound("assets/sounds/heal-up.mp3")  # Load sound file
        self.sound.set_volume(0.2 * GameSetup.effects_volume)

    def level_up(self):
        self.level += 1
        self.unscaled_image = pygame.image.load(f"assets/images/{self.upgrade_type}{self.level-1}.png")

        self.image = pygame.transform.scale(self.unscaled_image, (64, 64))
        self.image = pygame.transform.scale_by(self.image, GameSetup.width / 1920)
        self.image = pygame.Surface.convert_alpha(self.image)
        self.image_orig = self.image
        self.rect = self.image.get_rect()

    def update(self):
        self.pos = (self.pos[0] + self.velocity[0] * self.velocity_coefficient / 3,
                    self.pos[1] + self.velocity[1] * self.velocity_coefficient / 3)

        self.rect_non_rot.x = self.pos[0]
        self.rect_non_rot.y = self.pos[1]

        # rotation
        self.angle += self.angle_increment

        self.image = pygame.transform.rotate(self.image_non_rot, self.angle)
        self.rect = self.image.get_rect(center=self.rect_non_rot.center)
        self.mask = pygame.mask.from_surface(self.image)
        super().update()
