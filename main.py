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
    #   enemy
    enemy_group = pygame.sprite.Group()
    #   enemy spawn
    zarovka_spawner = EnemySpawner(enemy_group, "assets/images/zarovka.png", 5, None)
    tank_spawner = EnemySpawner(enemy_group, "assets/images/tank.png", 22, enemy_projectile_group)
    #   crosshair
    crosshair = Crosshair()
    crosshair_group = pygame.sprite.Group()
    crosshair_group.add(crosshair)
    #   explosions
    explosion_group = pygame.sprite.Group()

    # reset score
    score = 0

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
        if game_paused:     # game_pause is False from start and can be changed to True by pressing "p"
            # destroying crosshair, because I do not want to see him in background in pause menu
            crosshair.destroy()
            render_background(screen)
            render_health_bar(screen, player.max_hp, player.hp)
            render_score(screen, score)
            update_groups([player_projectile_group, enemy_projectile_group, player_group, enemy_group,explosion_group, crosshair_group],screen)
            # opening pause menu
            pause_menu(screen, clock, score)
            game_paused = False
            # re-creating cursor
            crosshair = Crosshair()
            crosshair_group = pygame.sprite.Group()
            crosshair_group.add(crosshair)

        # player death
        if not player_group and not explosion_group:
            break

        # rendering/update
        #   background
        render_background(screen)
        #   groups
        update_groups([player_projectile_group, enemy_projectile_group, player_group, enemy_group,explosion_group, crosshair_group], screen)
        #   enemy spawn
        zarovka_spawner.update(player.pos)
        tank_spawner.update(player.pos)
        #   collisions
        score_diff = 0
        score_diff += handle_collisions(player_group, enemy_group, False, explosion_group)
        score_diff += handle_collisions(player_projectile_group, enemy_group, True, explosion_group)
        handle_collisions(enemy_projectile_group, player_group, True, explosion_group)
        # handle_collisions(player_projectile_group, player_group, True, explosion_group)
        score += score_diff
        #   health bar
        render_health_bar(screen, player.max_hp, player.hp)
        #   score bar
        render_score(screen, score)
        #   overheat bar
        render_overheat_bar(screen, player.overheat, player.heat)
        # screen update (must be at the end of the loop before waiting functions!)
        pygame.display.flip()

        # FPS lock
        clock.tick(ScreenSetup.fps)

    # death text
    crosshair.disable()
    exit_text = font.render(f"SMRT, SCORE: {score}", True, (255, 255, 255))
    screen.blit(exit_text, (ScreenSetup.width/2, ScreenSetup.height/2))
    pygame.display.flip()
    time.sleep(2)
