import pygame
from screensetup import ScreenSetup

height = ScreenSetup.height  # finds height of screen
width = ScreenSetup.width  # finds width of screen


def render_health_bar(screen, max_hp, player_hp):
    # calculate health ratio
    ratio = player_hp / max_hp
    pygame.draw.rect(screen, "red", (35*width/40, 39*height/40, 47*width/400, height/70))
    pygame.draw.rect(screen, "green", (35*width/40, 39*height/40, (47*width/400)*ratio, height/70))