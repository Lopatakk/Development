import pygame


# This file is used to store functions for rendering and updating.
def render_background(screen):
    # This function renders the background image.
    screen.blit(pygame.image.load("space.png"), (0, 0))


def update_groups(groups, screen):
    # This function updates all the sprite groups in "groups" list. The order does matter, because the latter the group
    # is in the list, the upper it will apper.
    for group in groups:
        group.draw(screen)
        group.update()
