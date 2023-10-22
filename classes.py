import pygame
import sys
import numpy as np

screen_width = 640
screen_height = 640


class Triangle(pygame.sprite.Sprite):
    def __init__(self, picture_path):
        super().__init__()
        self.image_non_rot = pygame.image.load(picture_path)
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.rect.center = [screen_width/2, screen_height/2]
        self.pos = np.array([screen_width/2, screen_height/2])
        self.triangle_width = self.rect.height
        self.velocity = np.array([0, 0])
        self.max_velocity = np.array([100, 100])
        self.speed_coefficient = 0.1
        self.angle = self.rot_compute()
        self.hp = 100

    def update(self):
        # rotation
        self.angle = self.rot_compute()
        self.image = pygame.transform.rotate(self.image_non_rot, self.angle)
        self.rect = self.image.get_rect()

        # max speed
        if self.velocity[0] > self.max_velocity[0]:
            self.velocity[0] = self.max_velocity[0]
        elif self.velocity[0] < -self.max_velocity[0]:
            self.velocity[0] = -self.max_velocity[0]

        if self.velocity[1] > self.max_velocity[1]:
            self.velocity[1] = self.max_velocity[1]
        elif self.velocity[1] < -self.max_velocity[1]:
            self.velocity[1] = -self.max_velocity[1]

        # movement
        self.pos[0] += self.velocity[0] * self.speed_coefficient
        self.pos[1] += self.velocity[1] * self.speed_coefficient

        self.rect.center = self.pos

    def rot_compute(self):  # rotation computing
        dist_x = self.rect.center[0] - pygame.mouse.get_pos()[0]
        dist_y = self.rect.center[1] - pygame.mouse.get_pos()[1]
        if dist_y > 0:
            return np.rad2deg(np.arctan(dist_x/dist_y))
        elif dist_y < 0:
            return 180 + np.rad2deg(np.arctan(dist_x/dist_y))
        else:
            if dist_x == 0:
                return 90
            else:
                return -90


class Projectile(pygame.sprite.Sprite):
    def __init__(self, picturepath, triangle):
        super().__init__()
        self.image = pygame.image.load(picturepath)
        self.rect = self.image.get_rect()
        self.rect.center = triangle.rect.center
        self.angle = triangle.angle
        self.posx = self.rect.centerx - 1/2 * triangle.triangle_width * 0.95 * np.sin(np.deg2rad(triangle.angle))
        self.posy = self.rect.centery - 1/2 * triangle.triangle_width * 0.95 * np.cos(np.deg2rad(triangle.angle))

    def update(self):
        self.posx -= np.sin(np.deg2rad(self.angle)) * 5
        self.posy -= np.cos(np.deg2rad(self.angle)) * 5
        self.rect.center = [self.posx, self.posy]
        #  kill behind borders
        if self.posx > screen_width or self.posx < 0 or self.posy > screen_height or self.posy < 0:
            self.kill()
