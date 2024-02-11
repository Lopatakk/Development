import pygame
from screensetup import ScreenSetup


def check_buttons():
    key = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed(num_buttons=5)

    butt_array = [key[ScreenSetup.button_up], key[ScreenSetup.button_down],   # chápeš? jako zadek :D hahaha
                  key[ScreenSetup.button_left], key[ScreenSetup.button_right],
                  key[ScreenSetup.button_function_1], key[ScreenSetup.button_function_2],
                  mouse[0]]
    return butt_array
