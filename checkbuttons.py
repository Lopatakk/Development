import pygame
import numpy as np


def check_wsad():
    array = np.array([0, 0])
    key = pygame.key.get_pressed()
    if key[pygame.K_a]:
        array[0] += -1
    elif key[pygame.K_d]:
        array[0] += +1
    else:
        array[0] = 0

    if key[pygame.K_w]:
        array[1] += -1
    elif key[pygame.K_s]:
        array[1] += +1
    else:
        array[1] = 0
    return array
