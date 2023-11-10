import pygame
import sys
import time
import random
from player_ship import PlayerShip
from screensetup import ScreenSetup
from crosshair import Crosshair
from projectile import Projectile
from renderupdate import *
from enemy import Enemy
from checkbuttons import *
from collisions import handle_collisions
from enemy_spawn import EnemySpawner


# general setup
pygame.init()
clock = pygame.time.Clock()

# screen setup
screen = ScreenSetup.start_setup()

# text
font = pygame.font.Font('freesansbold.ttf', 30)



while True:     # main loop
    # creating sprites/groups
        # projectiles
    projectile_group = pygame.sprite.Group()
        # player
    player = PlayerShip()
    player_group = pygame.sprite.Group()
    player_group.add(player)
        # enemy
    enemy_group = pygame.sprite.Group()
        # enemy spawn
    zarovka_spawner = EnemySpawner(enemy_group, "zarovka", 5, 5, 35, 0.1, 1000, 100)  # Interval spawnování v sekundách
    tank_spawner = EnemySpawner(enemy_group, "tank", 5, 30, 20, 0.1, 4500, 100)
        # crosshair
    crosshair = Crosshair()
    crosshair_group = pygame.sprite.Group()
    crosshair_group.add(crosshair)

    # rendering
        # background
    render_background(screen)
        # groups
    update_groups([player_group, enemy_group], screen)
        # start text
    text_render = font.render("NEW GAME", True, (255, 255, 255))
    screen.blit(text_render, (ScreenSetup.width / 2.7, ScreenSetup.height / 4))

    # screen update (must be at the end of the loop before waiting functions!)
    pygame.display.flip()

    # wait
    time.sleep(0.5)

    while True:     # game loop
        for event in pygame.event.get():
            # closing window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # player death
        if not player_group:
            break

        # key/mouse pressing
            # WSAD
        player.velocity += check_wsad()
            # mouse
        mouse = pygame.mouse.get_pressed(num_buttons=5)
        if mouse[0]:
            projectile_group.add(player.shoot())

        # rendering/update
            # background
        render_background(screen)

            # groups
        update_groups([projectile_group, player_group, enemy_group, crosshair_group], screen)

            #enemy spawn updates
        zarovka_spawner.update(player.pos)
        tank_spawner.update(player.pos)
        # collisions
        handle_collisions(enemy_group, player_group)
        handle_collisions(projectile_group, enemy_group)
        #handle_collisions(projectile_group, player_group)


        # screen update (must be at the end of the loop before waiting functions!)
        pygame.display.flip()

        # FPS
        clock.tick(ScreenSetup.fps)

    # death text
    crosshair.disable()
    text_render = font.render("SMRT", True, (255, 255, 255))
    screen.blit(text_render, (ScreenSetup.width / 2, ScreenSetup.height / 2))
    # screen update
    pygame.display.flip()

    # wait
    time.sleep(2)
