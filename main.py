import pygame
import sys
import time
import random
from player_ship import PlayerShip
from screensetup import ScreenSetup
from crosshair import Crosshair
from projectile import Projectile
from renderupdate import *
from checkbuttons import *
from collisions import handle_collisions
from enemy_spawn import EnemySpawner

# general setup
#   pygame
pygame.init()
#   time
clock = pygame.time.Clock()
#   screen
screen = ScreenSetup.start_setup()
#   text font
font = pygame.font.Font('freesansbold.ttf', 30)


# main loop
while True:
    # creating sprites/groups
    #   projectiles
    projectile_group = pygame.sprite.Group()
    enemy_projectile_group = pygame.sprite.Group()
    #   player
    player = PlayerShip()
    player_group = pygame.sprite.Group()
    player_group.add(player)
    #   enemy
    enemy_group = pygame.sprite.Group()
    #   enemy spawn
    zarovka_spawner = EnemySpawner(enemy_group, "zarovka", 5, None)
    tank_spawner = EnemySpawner(enemy_group, "tank", 20, enemy_projectile_group)
    #   crosshair
    crosshair = Crosshair()
    crosshair_group = pygame.sprite.Group()
    crosshair_group.add(crosshair)

    # rendering before gameplay
    #   background
    render_background(screen)
    #   groups
    update_groups([player_group, enemy_group], screen)
    #   start text
    text_render = font.render("NEW GAME", True, (255, 255, 255))
    screen.blit(text_render, (ScreenSetup.width / 2, ScreenSetup.height / 2))

    # screen update (must be at the end of the loop before waiting functions!)
    pygame.display.flip()
    # wait
    time.sleep(1)

    # game loop
    while True:
        # closing window
        for event in pygame.event.get():
            # top right corner cross
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # esc
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        # player death
        if not player_group:
            break

        # key/mouse pressing
        #   WSAD
        player.velocity += check_wsad()
        #   mouse
        mouse = pygame.mouse.get_pressed(num_buttons=5)
        if mouse[0]:
            projectile_group.add(player.shoot())

        # rendering/update
        #   background
        render_background(screen)
        #   groups
        update_groups([projectile_group, player_group, enemy_group, crosshair_group], screen)
        #   enemy spawn
        zarovka_spawner.update(player.pos)
        tank_spawner.update(player.pos)
        #   collisions
        handle_collisions(enemy_group, player_group)
        handle_collisions(projectile_group, enemy_group)
        # handle_collisions(projectile_group, player_group)

        # screen update (must be at the end of the loop before waiting functions!)
        pygame.display.flip()

        # FPS lock
        clock.tick(ScreenSetup.fps)

    # death text
    crosshair.disable()
    font = pygame.font.Font(None, 36)
    exit_text = font.render("SMRT", True, (255, 255, 255))
    screen.blit(exit_text, (ScreenSetup.width/2, ScreenSetup.height/2))
    pygame.display.flip()
    time.sleep(2)
