import pygame
from screensetup import ScreenSetup


# This file is used to store functions for rendering and updating.
def render_background(screen):
    # This function renders the background image. It also uses the convert function to improve performance.
    background = pygame.image.load("assets/images/space.png")
    background = pygame.transform.scale(background, (ScreenSetup.width,ScreenSetup.height))
    background = pygame.Surface.convert(background)
    screen.blit(background, (0, 0))


def update_groups(groups, screen):
    # This function updates all the sprite groups in "groups" list. The order does matter, because the latter the group
    # is in the list, the upper it will apper.
    for group in groups:
        group.draw(screen)
        group.update()
