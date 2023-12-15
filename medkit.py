import pygame


class Medkit(pygame.sprite.Sprite):
    def __init__(self, pos, clock):
        super().__init__()
        self.type = "medkit"
        self.heal = 300
        self.pos = pos
        self.clock = clock
        self.time_on_screen = 0

        self.image = pygame.image.load("assets/images/medkit.png")
        self.image = pygame.Surface.convert_alpha(self.image)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = self.pos

        self.sound = pygame.mixer.Sound("assets/sounds/heal-up.mp3")
        self.sound.set_volume(0.2)

    def update(self):
        super().update()
        self.time_on_screen += self.clock.get_time()/1000
