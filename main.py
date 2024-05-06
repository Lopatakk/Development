import pygame
import sys
import time
from playerships.playerlight import PlayerLight
from playerships.playermid import PlayerMid
from playerships.playertank import PlayerTank
from gamesetup import GameSetup
from cursor import Cursor
from renderupdate import *
from collisions import *
from enemy_spawn import EnemySpawner
import menus
from background import Background
from itemspawn import ItemSpawner
from joystick_control import Joystick

# general setup
# pygame
pygame.init()
pygame.joystick.init()

# time
clock = pygame.time.Clock()

# screen
screen = GameSetup.start_setup()
# screen = pygame.display.set_mode((800, 600))  # Pavel_odkomentovávám pouze proto, abych viděl řádek

background = Background("Background", 3, (200, 350))
background_group = pygame.sprite.Group()
background_group.add(background)
overlay = None
background_copy = None

# collectable items
scrap_metal_count = 0
# upgrade = ShipUpgrade((0, 0), 'booster', True)
# upgrade1 = ShipUpgrade((0, 0), 'booster', True)
# upgrade2 = ShipUpgrade((0, 0), 'booster', True)
# upgrade3 = ShipUpgrade((0, 0), 'booster', True)
# storage_items = [upgrade, upgrade1, upgrade2, upgrade3]
storage_items = []
installed_items = {
    "weapons": None,
    "cooling": None,
    "shield": None,
    "repair_module": None,
    "booster": None
}

# text font
font = pygame.font.Font('assets/fonts/PublicPixel.ttf', 30)

# variables for menus
selected_number = 0
game_paused = False
waiting_for_player = False
game_paused_upgrade = False
game_main = True

# cursor
cursor = Cursor()
cursor_group = pygame.sprite.Group()
cursor_group.add(cursor)
cursor_group.update()

# controller
joystick = Joystick()

# sound
pygame.mixer.set_num_channels(30)

# background music
background_music = pygame.mixer.Sound("assets/sounds/background_music.mp3")
pygame.mixer.set_reserved(1)

# main loop
while True:
    # main_menu
    while selected_number == 0:
        if game_main:
            menus.main_menu(screen, joystick, cursor, clock, cursor_group)
            # ship_menu
            selected_number = menus.ship_menu(screen, joystick, cursor, clock, cursor_group)
            if selected_number == 1:
                selected_ship = PlayerLight
            elif selected_number == 2:
                selected_ship = PlayerMid
            elif selected_number == 3:
                selected_ship = PlayerTank
            if selected_number != 0:
                game_main = False
        else:
            # ship_menu
            selected_number = menus.ship_menu(screen, joystick, cursor, clock, cursor_group)
            if selected_number == 1:
                selected_ship = PlayerLight
            elif selected_number == 2:
                selected_ship = PlayerMid
            elif selected_number == 3:
                selected_ship = PlayerTank
            if selected_number == 0:
                game_main = True

    # variables for time in game + score
    time_in_game = 0
    score = 0

    # creating sprites/groups
    #   projectiles
    player_projectile_group = pygame.sprite.Group()
    enemy_projectile_group = pygame.sprite.Group()

    #   player
    player = selected_ship(joystick, player_projectile_group)
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

    # #   enemy spawners
    zarovka_spawner = EnemySpawner(enemy_group, "zarovka", 7, player)
    tank_spawner = EnemySpawner(enemy_group, "tank", 25, player, projectile_group=enemy_projectile_group)
    sniper_spawner = EnemySpawner(enemy_group, "sniper", 10, player, projectile_group=enemy_projectile_group)
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
    pygame.mixer.Channel(0).set_volume(0.04 * GameSetup.music_volume)
    pygame.mixer.Channel(0).play(background_music, 3)

    # setting
    storage_items = []
    installed_items = {
        "weapons": None,
        "cooling": None,
        "repair_module": None,
        "shield": None,
        "booster": None
    }
    player.ship_upgrade = {'weapons': 0,
                           'cooling': 0,
                           'repair_module': 0,
                           'shield': 0,
                           'booster': 0}

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
            if event.type == pygame.MOUSEMOTION or event.type == pygame.KEYDOWN:
                joystick.active = False
                cursor.active = True

        if joystick.active:
            cursor.active = False

            action = joystick.control_buttons()
            if action == 'settings' or action == 'exit':
                game_paused = True
        # controller
        joystick.update()

        # pause menu
        if game_paused:
            # game_pause is False from start and can be changed to True by pressing "esc"
            pygame.mixer.Channel(0).pause()
            cursor.set_cursor()

            # update the last frame
            update_groups([background_group, player_projectile_group, enemy_projectile_group, enemy_group,
                           player_group, explosion_group], screen)
            render_hud(screen, score, scrap_metal_count, [128, 128, 128], (player.time_alive - player.last_q_use) / player.q_cooldown,
                       player.is_q_action_on, (player.time_alive - player.last_e_use) / player.e_cooldown,
                       player.is_e_action_on, player.heat / player.overheat, player.is_overheated,
                       player.hp / player.max_hp)
            render_enemy_health_bar(screen, enemy_group)

            # pause surface
            overlay = pygame.Surface(screen.get_size())  # creates a new surface of the same dimensions as screen
            overlay = overlay.convert_alpha()  # making surface transparent
            background_copy = screen.copy()
            overlay.fill((0, 0, 0, 170))

            # opening pause menu
            if menus.pause_menu(screen, joystick, clock, score, player, cursor, cursor_group, storage_items, installed_items):
                game_main = True
                selected_number = 0
                game_paused = False
                break
            game_paused = False
            waiting_for_player = True

            # setting cursor to crosshair
            cursor.set_crosshair()
            pygame.mixer.Channel(0).unpause()
            pygame.mixer.Channel(0).set_volume(0.04 * GameSetup.music_volume)

        # upgrade menu
        if game_paused_upgrade:
            # game_paused_upgrade is False from start and can be changed to True by pressing "esc"
            cursor.set_cursor()

            # update the last frame
            update_groups([background_group, player_projectile_group, enemy_projectile_group, enemy_group,
                           player_group, explosion_group], screen)
            render_hud(screen, score, scrap_metal_count, [128, 128, 128],
                       (player.time_alive - player.last_q_use) / player.q_cooldown,
                       player.is_q_action_on, (player.time_alive - player.last_e_use) / player.e_cooldown,
                       player.is_e_action_on, player.heat / player.overheat, player.is_overheated,
                       player.hp / player.max_hp)
            render_enemy_health_bar(screen, enemy_group)

            # pause surface
            overlay = pygame.Surface(screen.get_size())  # creates a new surface of the same dimensions as screen
            overlay = overlay.convert_alpha()  # making surface transparent
            background_copy = screen.copy()
            overlay.fill((0, 0, 0, 170))

            # opening pause menu
            menus.upgrade_menu(screen, joystick, clock, player, cursor, cursor_group, storage_items, installed_items)
            game_paused_upgrade = False
            waiting_for_player = True

            # setting cursor to crosshair
            cursor.set_crosshair()

        # after pause or upgrade wait for player to make a move
        while waiting_for_player:
            # pressing any button resumes the game
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting_for_player = False
                if joystick.active:
                    for i in range(GameSetup.joysticks[0].get_numbuttons()):
                        if GameSetup.joysticks[0].get_button(i):
                            waiting_for_player = False
                            break
                    for i in range(GameSetup.joysticks[0].get_numaxes()):
                        if i < 4:
                            if abs(GameSetup.joysticks[0].get_axis(i)) > 0.5:
                                waiting_for_player = False
                                break
                        else:
                            if abs(GameSetup.joysticks[0].get_axis(i)) < 1:
                                waiting_for_player = False
                                break


            # render background
            screen.blit(background_copy, (0, 0))
            screen.blit(overlay, (0, 0))

            # render text
            pause_font = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(GameSetup.width / 38.4))
            title, text = GameSetup.set_language('pause')
            font_to_render = pause_font.render(text[3], True, (230, 230, 230))
            font_rect = font_to_render.get_rect()
            font_rect.centerx = GameSetup.width // 2
            font_rect.centery = GameSetup.height // 2
            screen.blit(font_to_render, font_rect)

            # locking the mouse cursor on the last position and render
            mouse_pos = pygame.mouse.get_pos()
            pygame.mouse.set_pos(mouse_pos)
            update_groups([cursor_group], screen)

            clock.tick(GameSetup.fps)
            pygame.display.flip()

        # player death
        if not player_group and not explosion_group:
            #   death_menu
            pygame.mixer.Channel(0).pause()
            cursor.set_cursor()
            if menus.death_menu(screen, joystick, cursor, clock, cursor_group, score, selected_number):
                game_main = True
            selected_number = 0
            scrap_metal_count = 0
            break

        # rendering/update
        #   groups
        update_groups([background_group, player_projectile_group, enemy_projectile_group, item_group, enemy_group,
                       player_group, explosion_group, cursor_group, spawner_group], screen)
        #   score and collisions
        score_diff = 0
        score_diff += handle_collisions(joystick, item_group, player_group, False, enemy_group, False, explosion_group)
        score_diff += handle_collisions(joystick, item_group, player_projectile_group, True, enemy_group, False, explosion_group)
        score += score_diff
        handle_collisions(joystick, item_group, enemy_projectile_group, True, player_group, False, explosion_group)
        handle_collisions(joystick, item_group, player_projectile_group, True, enemy_projectile_group, True, explosion_group)

        handle_item_collisions(item_group, enemy_group, storage_items, scrap_metal_count)

        outcome = handle_item_collisions(item_group, player_group, storage_items, scrap_metal_count)
        if outcome == "scrap_metal_collected":
            scrap_metal_count += 1
        elif outcome == "game_paused_upgrade":
            game_paused_upgrade = True

        #   HUD
        render_hud(screen, score, scrap_metal_count, [128, 128, 128], (player.time_alive - player.last_q_use) / player.q_cooldown,
                   player.is_q_action_on, (player.time_alive - player.last_e_use) / player.e_cooldown,
                   player.is_e_action_on, player.heat / player.overheat, player.is_overheated,
                   player.hp / player.max_hp)
        #   enemy scrap metal score
        render_enemy_health_bar(screen, enemy_group)
        #   enemy health bar
        render_enemy_health_bar(screen, enemy_group)

        if player.hp/player.max_hp <= 0.3 and GameSetup.danger_blinking:
            background.blink_danger(screen)

        # screen update (must be at the end of the loop before waiting functions!)
        pygame.display.flip()

        # FPS lock and adding time
        time_diff = clock.tick(GameSetup.fps) / 1000
        time_in_game += time_diff
        update_time([player_group, enemy_group, item_group, spawner_group], time_diff)

    # death text
    cursor.set_cursor()
    pygame.display.flip()
