import pygame.sprite
from screensetup import ScreenSetup


class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.screen_coefficient = ScreenSetup.width / 1920
        self.sound = pygame.mixer.Sound("assets/sounds/explosion.mp3")  # Load sound file
        self.sound.set_volume(0.8)
        pygame.mixer.find_channel(True).play(self.sound)

        for num in range(1, 9):
            img = pygame.image.load(f"assets/animations/explosion1/exp{num}.png")
            if size == 1:
                img = pygame.transform.scale(img, (150 * self.screen_coefficient, 150 * self.screen_coefficient))
            if size == 2:
                img = pygame.transform.scale(img, (300 * self.screen_coefficient, 300 * self.screen_coefficient))
            if size == 3:
                img = pygame.transform.scale(img, (500 * self.screen_coefficient, 500 * self.screen_coefficient))
            # add the image to the list
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.counter = 0

    def update(self):
        explosion_speed = 5
        # update explosion animation
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        # if the animation is complete, delete explosion
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()
