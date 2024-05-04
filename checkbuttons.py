import pygame
from gamesetup import GameSetup


def check_buttons():
    key = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed(num_buttons=5)

    butt_array = [key[GameSetup.button_up], key[GameSetup.button_down],   # chápeš? jako zadek :D hahaha
                  key[GameSetup.button_left], key[GameSetup.button_right],
                  key[GameSetup.button_function_1], key[GameSetup.button_function_2],
                  mouse[0]]
    return butt_array
