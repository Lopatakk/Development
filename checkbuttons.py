import pygame
import numpy as np


def check_buttons():
    key = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed(num_buttons=5)

    butt_array = [key[pygame.K_w], key[pygame.K_s], key[pygame.K_a], key[pygame.K_d],   # chápeš? jako zadek :D hahaha
                  key[pygame.K_q], key[pygame.K_e],
                  mouse[0]]
    return butt_array
