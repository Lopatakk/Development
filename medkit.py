import pygame


class Medkit(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.type = "medkit"
        self.heal = 300
        self.pos = pos
        self.time_alive = 0

        self.image = pygame.image.load("assets/images/medkit.png")
        self.image = pygame.Surface.convert_alpha(self.image)
        self.image_orig = self.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = self.pos

        self.has_thief = False

        self.sound = pygame.mixer.Sound("assets/sounds/heal-up.mp3")
        self.sound.set_volume(0.2)

        # animation
        self.animation_images = []
        for num in range(1, 7):
            img = pygame.image.load(f"assets/animations/medkit/medkit{num}.png")
            # add the image to the list
            self.animation_images.append(img)
        self.index = 0
        self.counter = -1
        self.animation_speed = 5
        self.last_animation_time = 0
        self.time_between_animations = 3

    def update(self):
        # animation
        elapsed_time = self.time_alive - self.last_animation_time
        if elapsed_time >= self.time_between_animations:
            self.counter = 0
            self.last_animation_time = self.time_alive
        if self.counter >= 0:
            self.counter += 1
        if self.counter >= self.animation_speed and self.index < len(self.animation_images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.animation_images[self.index]
        if self.index >= len(self.animation_images) - 1 and self.counter >= self.animation_speed:
            self.counter = -1
            self.index = 0
            self.image = self.image_orig

        super().update()
