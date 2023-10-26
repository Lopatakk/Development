import pygame


class Screen:
    fps = 60
    width = 640
    height = 640

    def __init__(self):
        pygame.display.set_mode((self.width, self.height))
