import pygame
import sys
import time
import random
from player_ship import PlayerShip
from screensetup import ScreenSetup
from cursor import Cursor
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
# screen = pygame.display.set_mode((1200, 800))  # Pavel_odkomentovávám pouze proto, abych viděl řádek
#   text font
font = pygame.font.Font('assets/fonts/PublicPixel.ttf', 30)
#   variables for menu
game_paused = False
#   cursor
cursor = Cursor()
cursor_group = pygame.sprite.Group()
cursor_group.add(cursor)
cursor_group.update()

# main loop
while True:
    # variables for time in game + score
    time_in_game = 0
    score = 0

    # creating sprites/groups
    #   projectiles
    player_projectile_group = pygame.sprite.Group()
    enemy_projectile_group = pygame.sprite.Group()
    #   player
    player = PlayerShip(clock, player_projectile_group)
    player_group = pygame.sprite.Group()
    player_group.add(player)
    #   enemy
    enemy_group = pygame.sprite.Group()
    #   enemy spawners
    zarovka_spawner = EnemySpawner(enemy_group, "zarovka", 7, clock, None, player)
    tank_spawner = EnemySpawner(enemy_group, "tank", 25, clock, enemy_projectile_group, player)
    sniper_spawner = EnemySpawner(enemy_group, "sniper", 10, clock, enemy_projectile_group, player)
    #   explosions
    explosion_group = pygame.sprite.Group()

    # rendering before gameplay
    #   background
    render_background(screen)
    #   groups
    update_groups([player_group, cursor_group], screen)
    #   start text
    text_render = font.render("NEW GAME", True, (255, 255, 255))
    screen.blit(text_render, (ScreenSetup.width / 2, ScreenSetup.height / 2))

    # setting cursor to crosshair
    cursor.set_crosshair()

    # screen update (must be at the end of the loop before waiting functions!)
    pygame.display.flip()

    # wait
    time.sleep(1)

    # gameplay loop
    while True:
        # KEYs and window cross functions
        for event in pygame.event.get():
            # opening pause menu - esc
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_paused = True

            # closing window - window cross
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # pause menu
        if game_paused:
            # game_pause is False from start and can be changed to True by pressing "esc"

            # destroying crosshair, because I do not want to see him in background in pause menu
            cursor.set_cursor()
            render_background(screen)
            render_health_bar(screen, player.max_hp, player.hp)
            # render_score(screen, score)
            render_overheat_bar(screen, player.overheat, player.heat, player.is_overheated)
            update_groups([player_projectile_group, enemy_projectile_group, enemy_group, player_group,
                           explosion_group], screen)
            # opening pause menu
            pause_menu(screen, clock, score, cursor_group)
            game_paused = False
            # setting cursor to crosshair
            cursor.set_crosshair()

        # player death
        if not player_group and not explosion_group:
            break

        # rendering/update
        #   background
        render_background(screen)
        #   groups
        update_groups([player_projectile_group, enemy_projectile_group, enemy_group, player_group, explosion_group,
                       cursor_group], screen)
        #   enemy spawn
        #zarovka_spawner.update()
        #tank_spawner.update()
        sniper_spawner.update()
        #   collisions and score
        score_diff = 0
        score_diff += handle_collisions(player_group, enemy_group, False, explosion_group)
        score_diff += handle_collisions(player_projectile_group, enemy_group, True, explosion_group)
        handle_collisions(enemy_projectile_group, player_group, True, explosion_group)
        score += score_diff
        #   health bar
        render_health_bar(screen, player.max_hp, player.hp)
        #   score bar
        render_score(screen, score, 128, 128, 128)
        #   overheat bar
        render_overheat_bar(screen, player.overheat, player.heat, player.is_overheated)

        # screen update (must be at the end of the loop before waiting functions!)
        pygame.display.flip()

        # FPS lock and adding time from last call of this function
        time_in_game += clock.tick(ScreenSetup.fps)

    # death text
    cursor.set_cursor()
    exit_text = font.render(f"SMRT, SCORE: {score}", True, (255, 255, 255))
    screen.blit(exit_text, (ScreenSetup.width/2, ScreenSetup.height/2))
    pygame.display.flip()
    time.sleep(2)
