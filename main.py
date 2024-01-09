import pygame
import sys
import time
from playerships.playerlight import PlayerLight
from playerships.playermid import PlayerMid
from playerships.playertank import PlayerTank
from screensetup import ScreenSetup
from cursor import Cursor
from renderupdate import *
from collisions import *
from enemy_spawn import EnemySpawner
import menus
from background import Background
from itemspawn import ItemSpawner

# general setup
#   pygame
pygame.init()
#   time
clock = pygame.time.Clock()
#   screen
screen = ScreenSetup.start_setup()
# screen = pygame.display.set_mode((1200, 800))  # Pavel_odkomentovávám pouze proto, abych viděl řádek
background_image = Background()
background_group = pygame.sprite.Group()
background_group.add(background_image)
#   text font
font = pygame.font.Font('assets/fonts/PublicPixel.ttf', 30)
#   variables for menus
game_paused = False
game_main = True
#   cursor
cursor = Cursor()
cursor_group = pygame.sprite.Group()
cursor_group.add(cursor)
cursor_group.update()
#   sound
pygame.mixer.set_num_channels(30)
#       background music
background_music = pygame.mixer.Sound("assets/sounds/background_music.mp3")
background_music.set_volume(0.04)
pygame.mixer.set_reserved(1)

# main loop
while True:
    # main_menu
    if game_main:
        menus.main_menu(screen, clock, cursor_group)
        game_main = False
    # ship_menu
    selected_number = menus.ship_menu(screen, clock, cursor_group)
    if selected_number == 1:
        selected_ship = PlayerLight
    elif selected_number == 2:
        selected_ship = PlayerMid
    elif selected_number == 3:
        selected_ship = PlayerTank
    # variables for time in game + score
    time_in_game = 0
    score = 0

    # creating sprites/groups
    #   projectiles
    player_projectile_group = pygame.sprite.Group()
    enemy_projectile_group = pygame.sprite.Group()
    #   player
    player = selected_ship(player_projectile_group)
    player_group = pygame.sprite.Group()
    player_group.add(player)
    #   enemy
    enemy_group = pygame.sprite.Group()
    #   items
    item_group = pygame.sprite.Group()
    #   item spawners
    spawner_group = pygame.sprite.Group()
    medkit_spawner = ItemSpawner(item_group, "medkit", 53, player)
    spawner_group.add(medkit_spawner)
    #   enemy spawners
    zarovka_spawner = EnemySpawner(enemy_group, "zarovka", 7, player)
    tank_spawner = EnemySpawner(enemy_group, "tank", 25, player, shot_group=enemy_projectile_group)
    sniper_spawner = EnemySpawner(enemy_group, "sniper", 10, player, shot_group=enemy_projectile_group)
    stealer_spawner = EnemySpawner(enemy_group, "stealer", 7, player, item_group=item_group)
    spawner_group.add(zarovka_spawner, tank_spawner, sniper_spawner, stealer_spawner)
    #   explosions
    explosion_group = pygame.sprite.Group()

    # rendering before gameplay
    #   groups
    update_groups([background_group, player_group, cursor_group], screen)

    # setting cursor to crosshair
    cursor.set_crosshair()

    # screen update (must be at the end of the loop before waiting functions!)
    pygame.display.flip()

    # background music start
    pygame.mixer.Channel(0).play(background_music, 3)

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
            pygame.mixer.Channel(0).pause()
            cursor.set_cursor()
            update_groups([background_group, player_projectile_group, enemy_projectile_group, enemy_group,
                           player_group, explosion_group], screen)
            render_hud(screen, score, [128, 128, 128], (player.time_alive - player.last_q_use) / player.q_cooldown,
                       player.is_q_action_on, (player.time_alive - player.last_e_use) / player.e_cooldown,
                       player.is_e_action_on, player.heat / player.overheat, player.is_overheated,
                       player.hp / player.max_hp)
            render_enemy_health_bar(screen, enemy_group)
            # opening pause menu
            if menus.pause_menu(screen, clock, score, cursor_group):
                game_main = True
                game_paused = False
                break
            game_paused = False
            # setting cursor to crosshair
            cursor.set_crosshair()
            pygame.mixer.Channel(0).unpause()

        # player death
        if not player_group and not explosion_group:
            #   death_menu
            cursor.set_cursor()
            if menus.death_menu(screen, clock, cursor_group, score):
                game_main = True
            break

        # rendering/update
        #   groups
        update_groups([background_group, player_projectile_group, enemy_projectile_group, item_group, enemy_group,
                       player_group, explosion_group, cursor_group, spawner_group], screen)
        #   score and collisions
        score_diff = 0
        score_diff += handle_collisions(player_group, False, enemy_group, False, explosion_group)
        score_diff += handle_collisions(player_projectile_group, True, enemy_group, False, explosion_group)
        score += score_diff
        handle_collisions(enemy_projectile_group, True, player_group, False, explosion_group)
        handle_collisions(player_projectile_group, True, enemy_projectile_group, True, explosion_group)
        handle_item_collisions(item_group, player_group)
        handle_item_collisions(item_group, enemy_group)
        #   HUD
        render_hud(screen, score, [128, 128, 128], (player.time_alive - player.last_q_use) / player.q_cooldown,
                   player.is_q_action_on, (player.time_alive - player.last_e_use) / player.e_cooldown,
                   player.is_e_action_on, player.heat / player.overheat, player.is_overheated,
                   player.hp / player.max_hp)
        #   enemy health bar
        render_enemy_health_bar(screen, enemy_group)

        # screen update (must be at the end of the loop before waiting functions!)
        pygame.display.flip()

        # FPS lock and adding time
        time_diff = clock.tick(ScreenSetup.fps) / 1000
        time_in_game += time_diff
        update_time([player_group, enemy_group, item_group, spawner_group], time_diff)

    # death text
    cursor.set_cursor()
    pygame.display.flip()
