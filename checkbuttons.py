import pygame
import numpy as np


def check_wsad():
    # Returns numpy array [x, y], where x and y have integer values which changes depending on pressing WSAD
    #
    # A is pressed -> x is decreased by 1
    # D is pressed -> x is increased by 1
    # neither A nor D or both at the same time are pressed -> x does not change
    # W is pressed -> y is decreased by 1
    # S is pressed -> y is increased by 1
    # neither W nor S or both at the same time are pressed -> y does not change
    #
    # Used for changing velocity of player's ship

    array = np.array([0, 0])
    key = pygame.key.get_pressed()

    if key[pygame.K_a] and key[pygame.K_d]:
        array[0] = 0
    elif key[pygame.K_a]:
        array[0] += -1
    elif key[pygame.K_d]:
        array[0] += +1
    else:
        array[0] = 0

    if key[pygame.K_w] and key[pygame.K_s]:
        array[0] = 0
    elif key[pygame.K_w]:
        array[1] += -1
    elif key[pygame.K_s]:
        array[1] += +1
    else:
        array[1] = 0
    return array
