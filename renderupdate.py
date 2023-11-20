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

def render_health_bar(screen, max_hp, player_hp):
    height = ScreenSetup.height  # finds height of screen
    width = ScreenSetup.width  # finds width of screen
    # calculate health ratio
    ratio = player_hp / max_hp
    pygame.draw.rect(screen, "red", (35*width/40, 39*height/40, 47*width/400, height/70))
    pygame.draw.rect(screen, "green", (35*width/40, 39*height/40, (47*width/400)*ratio, height/70))
