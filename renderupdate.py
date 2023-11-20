import pygame
from screensetup import ScreenSetup


# This file is used to store functions for rendering and updating.
def render_background(screen):
    """
    This function renders the background image. It also uses the convert function to improve performance.
    """
    background = pygame.image.load("assets/images/space.png")
    background = pygame.transform.scale(background, (ScreenSetup.width,ScreenSetup.height))
    background = pygame.Surface.convert(background)
    screen.blit(background, (0, 0))


def update_groups(groups, screen):
    """
    This function updates all the sprite groups in the input list. The order does matter, because the latter the group
    is in the list, the upper it will apper.
    """
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


def render_overheat_bar(screen, max_overheat, overheat):
    height = screen.get_height()  # finds height of screen
    width = screen.get_width()  # finds width of screen
    # calculate health ratio
    ratio = overheat / max_overheat
    pygame.draw.rect(screen, "red", (35*width/40, 38*height/40, 47*width/400, height/70))
    pygame.draw.rect(screen, "green", (35*width/40, 38*height/40, (47*width/400)*ratio, height/70))


def render_score(screen, score):
    height = ScreenSetup.height  # finds height of screen
    width = ScreenSetup.width  # finds width of screen
    font = pygame.font.Font('assets/fonts/PublicPixel.ttf', 30)
    text = font.render(str(score), True, (128, 128, 128))
    x = (width - text.get_width()) / 2 # score in the middle of the screen
    screen.blit(text, (x, height / 200))

