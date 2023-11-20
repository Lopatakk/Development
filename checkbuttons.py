import pygame
import numpy as np


def check_wsad():
    """
    Returns numpy array [x, y], where x and y have integer values which changes depending on pressing WSAD keys

    A is pressed -> x = -1
    D is pressed -> x = +1
    neither A nor D or both at the same time are pressed -> x = 0
    W is pressed -> y = +1
    S is pressed -> y = -1
    neither W nor S or both at the same time are pressed -> y = 0

    Used for changing velocity of player's ship.
    """

    array = np.array([0, 0])
    key = pygame.key.get_pressed()

    if key[pygame.K_a] and key[pygame.K_d]:
        array[0] = 0
    elif key[pygame.K_a]:
        array[0] = -1
    elif key[pygame.K_d]:
        array[0] = +1

    if key[pygame.K_w] and key[pygame.K_s]:
        array[0] = 0
    elif key[pygame.K_w]:
        array[1] = -1
    elif key[pygame.K_s]:
        array[1] = +1

    return array
