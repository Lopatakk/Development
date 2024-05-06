import pygame
from gamesetup import GameSetup
from pygame.sprite import Group
from pygame.surface import SurfaceType


# This file is used to store functions for rendering and updating.
def update_groups(groups, screen: SurfaceType) -> None:
    """
    This function updates all the sprite groups in the input list. The order does matter because the later the group
    is in the list, the later it will be rendered and the upper it will appear
    :param groups: List of groups to update
    :param screen: The surface the groups gets rendered on
    """
    for group in groups:
        group.update()
        group.draw(screen)


def update_time(groups, time_difference) -> None:
    """
    Adds the time difference to the time_alive variable of sprites in the groups
    :param groups: Sprite groups to update their time
    :param time_difference: The time difference
    :return: None
    """
    for group in groups:
        for thing in group:
            thing.time_alive += time_difference


def render_hud(screen: SurfaceType, score: int, scrap_metal_count: int, score_rgb, q_ratio: float, is_q_action_on: bool, e_ratio: float,
               is_e_action_on: bool, overheat_ratio: float, is_overheated: bool, health_ratio: float) -> None:
    """
    Renders score, q and e action charging bars, overheat and health bar on the screen
    :param scrap_metal_count: Number of colledcted scrap metal
    :param screen: Surface to render the HUD on
    :param score: The score value
    :param score_rgb: 3-item list with RGB values for color of the score text
    :param q_ratio: How much time since the last q action use / how much time does it take to charge it up
    :param is_q_action_on: Indicates if the q action is currently in use
    :param e_ratio: How much time since the last e action use / how much time does it take to charge it up
    :param is_e_action_on: Indicates if the e action is currently in use
    :param overheat_ratio: How much hot is the players ships gun / how much it can withstand
    :param is_overheated: Indicates if the players ships gun is overheated
    :param health_ratio: How much does the players ship has hp / maximum amount of the ships hp
    :return: None
    """
    # HUD = Head-up display
    # score
    font = pygame.font.Font('assets/fonts/PublicPixel.ttf', 30)
    text = font.render(str(score), True, (score_rgb[0], score_rgb[1], score_rgb[2]))
    x = (GameSetup.width - text.get_width()) / 2  # score in the middle of the screen
    screen.blit(text, (x, 10 + GameSetup.height / 200))

    # scrap metal
    x = GameSetup.width - 170  # score in the middle of the screen
    screen.blit(GameSetup.scrap_metal_icon, (x, GameSetup.height / 200))

    font = pygame.font.Font('assets/fonts/PublicPixel.ttf', 30)
    text = font.render(str(scrap_metal_count), True, (score_rgb[0], score_rgb[1], score_rgb[2]))
    screen.blit(text, (x + 70, 10 + GameSetup.height / 200))

    # overheat bar
    # bars proportions [x, y]
    bar_pos = [35 / 1920 * GameSetup.width, 990 / 1080 * GameSetup.height]
    bar_size = [230 / 1920 * GameSetup.width, 26 / 1080 * GameSetup.height]
    # calculating how much of the bar gets filled
    if overheat_ratio > 1:
        overheat_ratio = 1
    # drawing the color portion
    if is_overheated:
        pygame.draw.rect(screen, "red", (bar_pos[0], bar_pos[1], bar_size[0] * overheat_ratio, bar_size[1]))
    elif overheat_ratio > 0.75:
        pygame.draw.rect(screen, "orange", (bar_pos[0], bar_pos[1], bar_size[0] * overheat_ratio, bar_size[1]))
    elif overheat_ratio > 0.5:
        pygame.draw.rect(screen, "yellow", (bar_pos[0], bar_pos[1], bar_size[0] * overheat_ratio, bar_size[1]))
    else:
        pygame.draw.rect(screen, "green", (bar_pos[0], bar_pos[1], bar_size[0] * overheat_ratio, bar_size[1]))
    # render the image
    screen.blit(GameSetup.overheat_icon, [bar_pos[0] - 2/23 * bar_size[0], bar_pos[1] - 8/13 * bar_size[1]])

    # health bar
    # bars proportions
    bar_pos = [43 / 1920 * GameSetup.width, 1038 / 1080 * GameSetup.height]
    bar_size = [224 / 1920 * GameSetup.width, 26 / 1080 * GameSetup.height]
    # draw the bar
    pygame.draw.rect(screen, "red", (bar_pos[0], bar_pos[1], bar_size[0], bar_size[1]))
    pygame.draw.rect(screen, "green", (bar_pos[0], bar_pos[1], bar_size[0] * health_ratio, bar_size[1]))
    # render the image
    screen.blit(GameSetup.hp_icon, [bar_pos[0] - 1/8 * bar_size[0], bar_pos[1] - 7/26 * bar_size[1]])

    # q and e bars
    # bars proportions
    #   position [q_x_pos, e_x_pos, both_y_pos]
    bar_pos = [1725 / 1920 * GameSetup.width, 1825 / 1920 * GameSetup.width, 1004 / 1080 * GameSetup.height]
    #   size [both_width, both_height]
    bar_size = [62 / 1920 * GameSetup.width, 62 / 1920 * GameSetup.width]
    # ratios limitations
    if q_ratio > 1:
        q_ratio = 1
    if e_ratio > 1:
        e_ratio = 1
    # render the colour part
    #   q
    if is_q_action_on:
        pygame.draw.rect(screen, "red", (bar_pos[0], bar_pos[2], bar_size[0], bar_size[1]))
        # render the image
        screen.blit(GameSetup.q_action_icon_on, [bar_pos[0] - 1/14 * bar_size[0], bar_pos[2] - 2/3 * bar_size[1]])
    else:
        if q_ratio == 1:
            pygame.draw.rect(screen, "green", (bar_pos[0], bar_pos[2], bar_size[0], bar_size[1]))
        elif q_ratio > 0.5:
            pygame.draw.rect(screen, "yellow", (bar_pos[0], bar_pos[2] + (1-q_ratio) * bar_size[1], bar_size[0], bar_size[1] * q_ratio))
        else:
            pygame.draw.rect(screen, "orange", (bar_pos[0], bar_pos[2] + (1-q_ratio) * bar_size[1], bar_size[0], bar_size[1] * q_ratio))
        # render the image
        screen.blit(GameSetup.q_action_icon_off, [bar_pos[0] - 1/14 * bar_size[0], bar_pos[2] - 2/3 * bar_size[1]])
    #   e
    if is_e_action_on:
        pygame.draw.rect(screen, "red", (bar_pos[1], bar_pos[2], bar_size[0], bar_size[1]))
        # render the image
        screen.blit(GameSetup.e_action_icon_on, [bar_pos[1] - 1/14 * bar_size[0], bar_pos[2] - 2/3 * bar_size[1]])
    else:
        if e_ratio == 1:
            pygame.draw.rect(screen, "green", (bar_pos[1], bar_pos[2], bar_size[0], bar_size[1]))
        elif e_ratio > 0.5:
            pygame.draw.rect(screen, "yellow", (bar_pos[1], bar_pos[2] + (1-e_ratio) * bar_size[1], bar_size[0], bar_size[1] * e_ratio + 1))
        else:
            pygame.draw.rect(screen, "orange", (bar_pos[1], bar_pos[2] + (1-e_ratio) * bar_size[1], bar_size[0], bar_size[1] * e_ratio + 1))
        # render the image
        screen.blit(GameSetup.e_action_icon_off, [bar_pos[1] - 1/14 * bar_size[0], bar_pos[2] - 2/3 * bar_size[1]])


def render_score(screen: SurfaceType, score: int, r: int, g: int, b: int) -> None:
    """
    Renders score on the screen
    :param screen: Surface to render the score on
    :param score: The score value
    :param r: The value of red in the text color
    :param g: The value of green in the text color
    :param b: The value of blue in the text color
    :return: None
    """
    font = pygame.font.Font('assets/fonts/PublicPixel.ttf', 30)
    text = font.render(str(score), True, (r, g, b))
    x = (GameSetup.width - text.get_width()) / 2  # score in the middle of the screen
    screen.blit(text, (x, GameSetup.height / 200))

def render_scrapmetal(screen: SurfaceType, scrap_metal_count: int, r: int, g: int, b: int) -> None:
    """
    Renders score on the screen
    :param screen: Surface to render the score on
    :param score: The score value
    :param r: The value of red in the text color
    :param g: The value of green in the text color
    :param b: The value of blue in the text color
    :return: None
    """
    font = pygame.font.Font('assets/fonts/PublicPixel.ttf', 30)
    text = font.render(str(scrap_metal_count), True, (r, g, b))
    x = (GameSetup.width - text.get_width()) / 2  # score in the middle of the screen
    screen.blit(text, (x, GameSetup.height / 200))

def render_enemy_health_bar(screen: SurfaceType, enemy_group: Group) -> None:
    """
    Renders small health bars under enemy ships
    :param screen: Surface to render the bars on
    :param enemy_group: A Sprite group of enemy ships the bars will be rendered at/for
    :return: None
    """
    # bars proportions
    bar_size = [1/33 * GameSetup.width, 1/180 * GameSetup.height]

    for ship in enemy_group:
        if ship.hp != ship.max_hp:
            # bar position
            bar_pos = [ship.pos[0] - 1/2 * bar_size[0], ship.pos[1] + 2/3 * ship.height]
            # ratio computing
            ratio = ship.hp / ship.max_hp
            # drawing
            pygame.draw.rect(screen, "red", (bar_pos[0], bar_pos[1], bar_size[0], bar_size[1]))
            pygame.draw.rect(screen, "green", (bar_pos[0], bar_pos[1], bar_size[0] * ratio, bar_size[1]))
