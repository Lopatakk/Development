import pygame
from screensetup import ScreenSetup


# This file is used to store functions for rendering and updating.
def render_background(screen):
    """
    This function renders the background image. It also uses the convert function to improve performance.
    :param screen: the surface the background gets rendered on
    """
    background = pygame.image.load("assets/images/space.png")
    background = pygame.transform.scale(background, (ScreenSetup.width, ScreenSetup.height))
    background = pygame.Surface.convert(background)
    screen.blit(background, (0, 0))


def update_groups(groups, screen):
    """
    This function updates all the sprite groups in the input list. The order does matter, because the latter the group
    is in the list, the upper it will apper.
    :param groups: list of groups to update
    :param screen: the surface the groups gets rendered on
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


def render_overheat_bar(screen, overheat: int, heat: float):
    """
    Renders overheat bar for ship in the lower left corner of the screen (above the hp bar). Green portion of the bar
    indicates how much heated ship's gun is and the red portion indicates how hotter it can get.
    :param screen: the surface the bar gets rendered on
    :param overheat: the max heat the gun can handle
    :param heat: current amount of heat the gun has
    :return: nothing
    """
    # getting screen size
    width = screen.get_width()
    height = screen.get_height()
    # calculating how much of the bar gets filled
    ratio = heat / overheat
    # drawing red background of the bar
    pygame.draw.rect(screen, "red", (35/40*width, 38/40*height, 47/400*width, 1/70*height))
    # drawing the green portion
    pygame.draw.rect(screen, "green", (35/40*width, 38/40*height, (47/400*width)*ratio, 1/70*height))


def render_score(screen, score, R, G, B):
    height = ScreenSetup.height  # finds height of screen
    width = ScreenSetup.width  # finds width of screen
    font = pygame.font.Font('assets/fonts/PublicPixel.ttf', 30)
    text = font.render(str(score), True, (R, G, B))
    x = (width - text.get_width()) / 2 # score in the middle of the screen
    screen.blit(text, (x, height / 200))

