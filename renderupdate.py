import pygame
from screensetup import ScreenSetup
from pygame.sprite import Group
from pygame.surface import SurfaceType


# This file is used to store functions for rendering and updating.
def update_groups(groups, screen: SurfaceType):
    """
    This function updates all the sprite groups in the input list. The order does matter, because the latter the group
    is in the list, the upper it will appear.
    :param groups: List of groups to update
    :param screen: The surface the groups gets rendered on
    """
    for group in groups:
        group.update()
        group.draw(screen)


def update_time(groups, time_difference):
    for group in groups:
        for thing in group:
            thing.time_alive += time_difference


def render_hud(screen: SurfaceType, score: int, score_rgb, q_ratio, is_q_action_on, e_ratio, is_e_action_on,
               overheat_ratio, is_overheated: bool, health_ratio):
    # HUD = Head-up display
    # score
    font = pygame.font.Font('assets/fonts/PublicPixel.ttf', 30)
    text = font.render(str(score), True, (score_rgb[0], score_rgb[1], score_rgb[2]))
    x = (ScreenSetup.width - text.get_width()) / 2  # score in the middle of the screen
    screen.blit(text, (x, ScreenSetup.height / 200))

    # q and e bars
    # bars proportions
    #   position [both_x_pos, q_y_pos, e_y_pos]
    bars_pos = [3 / 400 * ScreenSetup.width, 38 / 40 * ScreenSetup.height, 39 / 40 * ScreenSetup.height]
    #   size [both_width, both_height]
    bars_size = [47 / 400 * ScreenSetup.width, 1 / 70 * ScreenSetup.height]
    # ratios limitations
    if q_ratio > 1:
        q_ratio = 1
    if e_ratio > 1:
        e_ratio = 1
    # render gray back rects
    #   q
    pygame.draw.rect(screen, "gray", (bars_pos[0], bars_pos[1], bars_size[0], bars_size[1]))
    #   e
    pygame.draw.rect(screen, "gray", (bars_pos[0], bars_pos[2], bars_size[0], bars_size[1]))
    # render the colour part
    #   q
    if is_q_action_on:
        pygame.draw.rect(screen, "red", (bars_pos[0], bars_pos[1], bars_size[0], bars_size[1]))
    elif q_ratio == 1:
        pygame.draw.rect(screen, "green", (bars_pos[0], bars_pos[1], bars_size[0], bars_size[1]))
    elif q_ratio > 0.5:
        pygame.draw.rect(screen, "yellow", (bars_pos[0], bars_pos[1], bars_size[0] * q_ratio, bars_size[1]))
    else:
        pygame.draw.rect(screen, "orange", (bars_pos[0], bars_pos[1], bars_size[0] * q_ratio, bars_size[1]))
    #   e
    if is_e_action_on:
        pygame.draw.rect(screen, "red", (bars_pos[0], bars_pos[2], bars_size[0], bars_size[1]))
    elif e_ratio == 1:
        pygame.draw.rect(screen, "green", (bars_pos[0], bars_pos[2], bars_size[0], bars_size[1]))
    elif e_ratio > 0.5:
        pygame.draw.rect(screen, "yellow", (bars_pos[0], bars_pos[2], bars_size[0] * e_ratio, bars_size[1]))
    else:
        pygame.draw.rect(screen, "orange", (bars_pos[0], bars_pos[2], bars_size[0] * e_ratio, bars_size[1]))

    # overheat bar
    # bars proportions [x, y]
    bar_pos = [35 / 40 * ScreenSetup.width, 38 / 40 * ScreenSetup.height]
    bar_size = [47 / 400 * ScreenSetup.width, 1 / 70 * ScreenSetup.height]
    # calculating how much of the bar gets filled
    if overheat_ratio > 1:
        overheat_ratio = 1
    # drawing gray background of the bar
    pygame.draw.rect(screen, "gray", (bar_pos[0], bar_pos[1], bar_size[0], bar_size[1]))
    # drawing the color portion
    if is_overheated:
        pygame.draw.rect(screen, "red", (bar_pos[0], bar_pos[1], bar_size[0] * overheat_ratio, bar_size[1]))
    elif overheat_ratio > 0.75:
        pygame.draw.rect(screen, "orange", (bar_pos[0], bar_pos[1], bar_size[0] * overheat_ratio, bar_size[1]))
    elif overheat_ratio > 0.5:
        pygame.draw.rect(screen, "yellow", (bar_pos[0], bar_pos[1], bar_size[0] * overheat_ratio, bar_size[1]))
    else:
        pygame.draw.rect(screen, "green", (bar_pos[0], bar_pos[1], bar_size[0] * overheat_ratio, bar_size[1]))

    # health bar
    # bars proportions
    bar_pos = [35/40 * ScreenSetup.width, 39/40 * ScreenSetup.height]
    bar_size = [47/400 * ScreenSetup.width, 1/70 * ScreenSetup.height]
    # draw the bar
    pygame.draw.rect(screen, "red", (bar_pos[0], bar_pos[1], bar_size[0], bar_size[1]))
    pygame.draw.rect(screen, "green", (bar_pos[0], bar_pos[1], bar_size[0] * health_ratio, bar_size[1]))


def render_score(screen: SurfaceType, score, r, g, b):
    font = pygame.font.Font('assets/fonts/PublicPixel.ttf', 30)
    text = font.render(str(score), True, (r, g, b))
    x = (ScreenSetup.width - text.get_width()) / 2  # score in the middle of the screen
    screen.blit(text, (x, ScreenSetup.height / 200))


def render_enemy_health_bar(screen: SurfaceType, enemy_group: Group):
    # bars proportions
    bar_size = [1/33 * ScreenSetup.width, 1/180 * ScreenSetup.height]

    for ship in enemy_group:
        if ship.hp != ship.max_hp:
            # bar position
            bar_pos = [ship.pos[0] - 1/2 * bar_size[0], ship.pos[1] + 2/3 * ship.height]
            # ratio computing
            ratio = ship.hp / ship.max_hp
            # drawing
            pygame.draw.rect(screen, "red", (bar_pos[0], bar_pos[1], bar_size[0], bar_size[1]))
            pygame.draw.rect(screen, "green", (bar_pos[0], bar_pos[1], bar_size[0] * ratio, bar_size[1]))
