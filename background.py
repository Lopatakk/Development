import pygame
from screensetup import ScreenSetup
import random


class Background(pygame.sprite.Sprite):
    def __init__(self, background_type, frames_num, rand):
        super().__init__()
        self.images = []
        self.rand = rand
        for num in range(frames_num):
            img = pygame.image.load(f"assets/animations/background/{background_type}{num}.png")
            img = pygame.transform.scale(img, (ScreenSetup.width, ScreenSetup.height))
            img = pygame.Surface.convert(img)
            # add the image to the list
            self.images.append(img)
        self.counter = 0
        self.animation_speed = random.randint(self.rand[0], self.rand[1])

        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = [0, 0]

        # blinking parameters
        self.red_surface = pygame.Surface((ScreenSetup.width, ScreenSetup.height), pygame.SRCALPHA)
        self.fade_speed = 2
        self.pulse_pause_duration = 20
        self.current_alpha = 0
        self.is_fading_out = False
        self.blink_count = 0
        self.pause_count = 0

    def update(self):
        self.counter += 1
        if self.counter >= self.animation_speed:
            index = random.randint(0, len(self.images) - 1)
            self.image = self.images[index]
            self.animation_speed = random.randint(self.rand[0], self.rand[1])
            self.counter = 0
        super().update()

    def blink_danger(self, screen):
        if self.blink_count < 2:
            if self.is_fading_out:
                self.current_alpha -= self.fade_speed
                if self.current_alpha <= 0:
                    self.current_alpha = 0
                    self.is_fading_out = False
                    self.blink_count += 1
            else:
                self.current_alpha += self.fade_speed
                if self.current_alpha >= 30:
                    self.current_alpha = 30
                    self.is_fading_out = True
        elif self.pause_count < self.pulse_pause_duration:
            self.pause_count += 1
        else:
            self.blink_count = 0
            self.pause_count = 0

        self.red_surface.fill((255, 0, 0, self.current_alpha))
        screen.blit(self.red_surface, (0, 0))

