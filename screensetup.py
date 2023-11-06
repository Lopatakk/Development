import pygame


class ScreenSetup:
    # This class is used to store screen parameters and functions

    # Screen parameters:
    width = 1500
    height = 1000
    fps = 60

    def __init__(self):
        # This is just there, so it can be a class :)
        pass

    @classmethod
    def start_setup(cls):
        # This function "sets the screen on". The object does not have to be created, it can be called anytime (but it
        # really has to be called only at the beginning of the code).
        return pygame.display.set_mode((cls.width, cls.height))
