import pygame
from gamesetup import GameSetup


class EventHorizonPulse(pygame.sprite.Sprite):
    def __init__(self, ship):
        super().__init__()

        self.speed = int(40 * GameSetup.width / 1920)
        self.dmg = 10000
        self.thickness = int(40 * GameSetup.width / 1920)

        self.screen = ship.screen

        start_size = int(max(ship.width, ship.height))
        self.parameter = start_size/2
        self.start_pos = ship.pos
        self.image_not_shown = pygame.Surface((start_size, start_size))
        self.image_not_shown.fill("green")
        pygame.draw.circle(self.image_not_shown, "black", (self.parameter, self.parameter), self.parameter, self.thickness)
        pygame.draw.circle(self.screen, "black", self.start_pos, self.parameter, self.thickness)
        self.image_not_shown.set_colorkey("green")
        self.image_not_shown = pygame.Surface.convert_alpha(self.image_not_shown)
        self.rect = self.image_not_shown.get_rect()
        self.rect.center = self.start_pos
        self.mask = pygame.mask.from_surface(self.image_not_shown)

        self.image = pygame.Surface((1, 1))
        self.pos = [-70, -70]

        self.type = "event_horizon_pulse"

        self.sound = pygame.mixer.Sound("assets/sounds/event_horizon_pulse.mp3")
        self.sound.set_volume(1 * GameSetup.effects_volume)
        pygame.mixer.find_channel(False).play(self.sound)

    def update(self):
        self.image_not_shown = pygame.Surface((self.image_not_shown.get_width() + self.speed,
                                               self.image_not_shown.get_width() + self.speed))
        self.parameter = self.image_not_shown.get_width()/2
        self.image_not_shown.fill("green")
        pygame.draw.circle(self.image_not_shown, "black", (self.parameter, self.parameter), self.parameter,
                           self.thickness)
        pygame.draw.circle(self.screen, "black", self.start_pos, self.parameter, self.thickness)
        self.image_not_shown.set_colorkey("green")
        self.rect = self.image_not_shown.get_rect()
        self.rect.center = self.start_pos
        self.mask = pygame.mask.from_surface(self.image_not_shown)

    def kill(self):
        super().kill()
        self.mask = None
