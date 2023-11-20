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
from pause_menu import pause_menu
from health_bar import render_health_bar

# general setup
#   pygame
pygame.init()
#   time
clock = pygame.time.Clock()
#   screen
screen = ScreenSetup.start_setup()
ScreenSetup.width, ScreenSetup.height = pygame.display.Info().current_w, pygame.display.Info().current_h
# screen = pygame.display.set_mode((800, 600))  # Pavel_odkomentovávám pouze proto, abych viděl řádek
#   text font
font = pygame.font.Font('assets/fonts/PublicPixel.ttf', 30)
#   variables for menu
game_paused = False

# main loop
while True:
    # creating sprites/groups
    #   projectiles
    player_projectile_group = pygame.sprite.Group()
    enemy_projectile_group = pygame.sprite.Group()
    #   player
    player = PlayerShip(player_projectile_group)
    player_group = pygame.sprite.Group()
    player_group.add(player)
    max_hp = player.hp      # players max hp at the beginning
    #   enemy
    enemy_group = pygame.sprite.Group()
    #   enemy spawn
    zarovka_spawner = EnemySpawner(enemy_group, "assets/images/zarovka.png", 5, None)
    tank_spawner = EnemySpawner(enemy_group, "assets/images/tank.png", 22, enemy_projectile_group)
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
        # KEYs function
        for event in pygame.event.get():
            # opening pause menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_paused = True

            # closing window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # pause detection
        if game_paused:
            # game_paused is False from start and can be changed to True by pressing "p". After that the game will stop
            # and pause menu appears.
            pause_menu(screen, clock)
            game_paused = False

        # player death
        if not player_group:
            break

        # rendering/update
        #   background
        render_background(screen)
        #   groups
        update_groups([player_projectile_group, enemy_projectile_group, player_group, enemy_group, crosshair_group], screen)
        #   enemy spawn
        zarovka_spawner.update(player.pos)
        tank_spawner.update(player.pos)
        #   collisions
        handle_collisions(enemy_group, player_group)
        handle_collisions(player_projectile_group, enemy_group)
        handle_collisions(enemy_projectile_group, player_group)
        # handle_collisions(projectile_group, player_group)
        #   health bar
        render_health_bar(screen, max_hp, player.hp)

        # screen update (must be at the end of the loop before waiting functions!)
        pygame.display.flip()

        # FPS lock
        clock.tick(ScreenSetup.fps)

    # death text
    crosshair.disable()
    exit_text = font.render("SMRT", True, (255, 255, 255))
    screen.blit(exit_text, (ScreenSetup.width/2, ScreenSetup.height/2))
    pygame.display.flip()
    time.sleep(2)
