import pygame


class ScreenSetup:
    fps = 60
    width = 640
    height = 640

    def __init__(self):
        pass

    @classmethod
    def start_setup(cls):
        return pygame.display.set_mode((cls.width, cls.height))
