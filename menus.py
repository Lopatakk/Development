import pygame
import button
from renderupdate import *
from leaderboard import *
import datetime
import drawText
from slider import Slider
from ship_upgrade import *
from collisions import *

from enemy_spawn import EnemySpawner
from playerships.mini_player import *
from background import Background
from itemspawn import ItemSpawner
from cursor import Cursor


def settings_menu(screen, clock, cursor_group, background, environment):
    width, height = screen.get_size()
    #   fonts
    font_title = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.05 * width))  # loading font
    font_subTitle = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.018 * width))  # loading font
    font_height = font_subTitle.get_height()

    #   surface and background
    # surface
    surface = pygame.Surface(screen.get_size())  # creates a new surface of the same dimensions as screen
    surface = surface.convert_alpha()  # making surface transparent

    # background
    # fill the whole screen with black transparent color
    if environment == "main":
        surface.fill((0, 0, 0, 80))
    else:
        surface.fill((0, 0, 0, 170))

        # languages
    # flags
    flags = ['eng', 'cz', 'fr', 'de', 'esp']
    flag_rects = []
    flags_images = []
    flag_width = 0
    flag_height = 0
    on_language = False
    flag_offset_x = 20
    flag_offset_y = 20
    for i, flag in enumerate(flags):
        flag_surf = pygame.image.load(f"assets/images/languages/{flag}.png").convert_alpha()
        flag_width = int(flag_surf.get_width() * 0.8)
        flag_height = int(flag_surf.get_height() * 0.8)
        flag_surf = pygame.transform.scale(flag_surf, (flag_width, flag_height))
        flag_rect = pygame.rect.Rect(1400, 30 + (flag_offset_y + flag_height) * i, flag_width, flag_height)
        flags_images.append(flag_surf)
        flag_rects.append(flag_rect)

    # flags background
    background_flag_width = flag_width + flag_offset_x
    background_flag_height = len(flags_images) * (flag_height + flag_offset_y)
    flag_background = pygame.Surface((int(background_flag_width), int(background_flag_height)))
    flag_background.set_alpha(50)
    flag_background.fill('gray')
    flag_background_rect = flag_background.get_rect()
    flag_background_rect.x = 1400 - flag_offset_y / 2
    flag_background_rect.y = 30 - flag_offset_y / 2

    #   volume
    min_value = 0
    max_value = 10
    with open("settings.json", "r") as settings_file:
        settings = json.load(settings_file)
    music_volume = settings["music_volume"]
    effects_volume = settings["effects_volume"]
    danger_blinking = settings["danger_blinking"]

    # text
    title, game_text = GameSetup.set_language("settings")

    #   create button instances
    danger_button_on = button.Button(255, 620, "assets/images/switch_on0.png",
                                     "assets/images/switch_on1.png", 0.1, 0.05, 0.025, '', screen,
                                     "assets/sounds/button_click.mp3", 0.2)
    danger_button_off = button.Button(255, 620, "assets/images/switch_off0.png",
                                      "assets/images/switch_off1.png", 0.1, 0.05, 0.025, '', screen,
                                      "assets/sounds/button_click.mp3", 0.2)
    back_button = button.Button(16 * width / 20, 70 * height / 80, "assets/images/button_01.png",
                                "assets/images/button_02.png", 0.15, 0.05, 0.025, game_text[3], screen,
                                "assets/sounds/button_click.mp3", 0.2)

    # percentage
    percentageMusic = ((music_volume - min_value) / (max_value - min_value)) * 100
    percentageEffects = ((effects_volume - min_value) / (max_value - min_value)) * 100
    #   sliders
    sliderMusic = Slider((3.6 * width / 20), (27 * height / 80 + font_height * 2), (width * 0.375), (width * 0.015),
                         min_value, max_value, percentageMusic)
    sliderEffects = Slider((3.6 * width / 20), (37 * height / 80 + font_height * 2), (width * 0.375), (width * 0.015),
                           min_value, max_value, percentageEffects)

    while True:
        mouse_pressed = False
        mouse_pos = pygame.mouse.get_pos()

        # background
        screen.blit(background, (0, 0))
        screen.blit(surface, (0, 0))

        # button update
        back_button.update_text(game_text[3])

        # render languages
        if on_language:
            screen.blit(flag_background, flag_background_rect)
            for i, flag in enumerate(flags_images):
                screen.blit(flag, flag_rects[i])
        else:
            language_index = GameSetup.all_languages.index(GameSetup.language)
            screen.blit(flags_images[language_index], flag_rects[0])

        #   text "Settings"
        screen.blit(font_title.render(title, True, (230, 230, 230)), (3.6 * width / 20, 3.4 * height / 20))

        #   changing volume
        screen.blit(font_subTitle.render(game_text[0], True, (230, 230, 230)), (3.6 * width / 20, 27 * height / 80))
        screen.blit(font_subTitle.render(game_text[1], True, (230, 230, 230)), (3.6 * width / 20, 37 * height / 80))

        # danger blinking
        screen.blit(font_subTitle.render(game_text[2], True, (230, 230, 230)),
                    (3.6 * width / 20, 52 * height / 80))

        #   BUTTON
        if back_button.draw_button_and_text(screen):
            pygame.mixer.Channel(3).stop()
            return

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # to cancel
                pygame.mixer.Channel(3).stop()
                return
            elif event.type == pygame.MOUSEBUTTONUP and not mouse_pressed:
                mouse_pressed = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # switching danger blinking
                mouse_pressed = False
                with open("settings.json", "w") as settings_file:
                    json.dump(settings, settings_file, indent=4)
                GameSetup.update()

                # clicking on languages
                if on_language:
                    for i, rect in enumerate(flag_rects):
                        if rect.collidepoint(mouse_pos):
                            GameSetup.language = GameSetup.all_languages[i]
                            on_language = False
                            title, game_text = GameSetup.set_language("settings")
                            settings["language"] = GameSetup.language
                            with open("settings.json", "w") as settings_file:
                                json.dump(settings, settings_file, indent=4)
                elif flag_rects[0].collidepoint(mouse_pos):
                    if on_language:
                        on_language = False
                    else:
                        on_language = True

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:  # to quit game
                quit()

        if danger_blinking:
            if danger_button_on.draw_button_and_text(screen):
                settings["danger_blinking"] = False
                danger_blinking = False
                with open("settings.json", "w") as settings_file:
                    json.dump(settings, settings_file, indent=4)
                GameSetup.update()
        else:
            if danger_button_off.draw_button_and_text(screen):
                settings["danger_blinking"] = True
                danger_blinking = True
                with open("settings.json", "w") as settings_file:
                    json.dump(settings, settings_file, indent=4)
                GameSetup.update()

        #   volume
        # music
        sliderMusic.update(mouse_pressed, settings, "music_volume")
        sliderMusic.draw(screen)

        # effects
        sliderEffects.update(mouse_pressed, settings, "effects_volume")
        sliderEffects.draw(screen)

        if danger_blinking:
            if danger_button_on.draw_button_and_text(screen):
                settings["danger_blinking"] = False
                danger_blinking = False
        else:
            if danger_button_off.draw_button_and_text(screen):
                settings["danger_blinking"] = True
                danger_blinking = True

        # cursor
        update_groups([cursor_group], screen)

        clock.tick(GameSetup.fps)
        pygame.display.flip()

def save_name_menu(screen, clock, cursor_group, score, ship_number):
    width, height = screen.get_size()
    font_title = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.05 * width))
    font_info = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.01 * width))
    #   surface and background
    # surface
    surface = pygame.Surface(screen.get_size())  # creates a new surface of the same dimensions as screen
    surface = surface.convert_alpha()  # making surface transparent
    surface.fill((0, 0, 0, 230))  # fill the whole screen with black transparent color
    # background
    background = pygame.image.load("assets/images/Background.png")
    background = pygame.transform.scale(background, (width, height))
    background = pygame.Surface.convert(background)
    #   create button instances
    save_button = button.Button(3.6 * width / 20, 50 * height / 80, "assets/images/button_01.png",
                                "assets/images/button_02.png", 0.3, 0.05, 0.025, 'Save', screen,
                                "assets/sounds/button_click.mp3", 0.2)
    cancel_button = button.Button(3.6 * width / 20, 59 * height / 80, "assets/images/button_01.png",
                                  "assets/images/button_02.png", 0.3, 0.05, 0.025, 'Cancel', screen,
                                  "assets/sounds/button_click.mp3", 0.2)
    #   the current date
    date = f'{datetime.datetime.now().date()}'
    #   name input
    user_name = ''
    font_input = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.025 * width))
    text_box = pygame.Rect(3.6 * width / 20, 28 * height / 80, width / 2.5, width / 20)
    #   selected ship from nuber
    if ship_number == 1:
        selected_ship = "Light"
    elif ship_number == 2:
        selected_ship = "Mid"
    else:
        selected_ship = "Tank"
    while True:
        screen.blit(background, (0, 0))
        screen.blit(surface, (0, 0))
        #   text "Your name"
        screen.blit(font_title.render("Your name", True, (230, 230, 230)), (3.6 * width / 20, 3.4 * height / 20))
        #   button
        # if there is some input text
        if len(user_name) > 0:
            if save_button.draw_button_and_text(screen):
                save(highscore)
                return True
        if cancel_button.draw_button_and_text(screen):
            return False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # to cancel
                return False
            if event.type == pygame.KEYDOWN:
                #   if there is some input text
                if len(user_name) > 0:
                    if event.key == pygame.K_RETURN:
                        save(highscore)
                        return True
                    if event.key == pygame.K_BACKSPACE:
                        if len(user_name) > 0:
                            user_name = user_name[:-1]
                #   adding text
                # only letters, numbers, ".", "-" and maximum of 15 characters
                if len(user_name) < 15 and (event.unicode.isalnum() or event.unicode in ['.', '-']):
                    user_name += event.unicode
        #   data to save
        highscore = [[user_name, score, selected_ship, date]]
        #   rendering input
        # draw box around for text input
        pygame.draw.rect(screen, (230, 230, 230), text_box, int(width / 300))
        # input text
        text_surface = font_input.render(user_name, True, (230, 230, 230))
        # box is getting bigger with text (min. width, if is text wider, it is adding more width)
        text_box.w = max(width / 2.5, text_surface.get_width() + width / 50)
        # text
        text_rect = text_surface.get_rect()
        text_rect.centery = text_box.centery  # to get y center of text to y center of box
        text_rect.x = text_box.x + width / 100  # to get left side of text to wanted position
        # draw input text on wanted position
        screen.blit(text_surface, text_rect)
        # info about characters and rules when writing name
        screen.blit(font_info.render("maximum 15 characters", True, (150, 150, 150)),
                    (3.6 * width / 20, text_box.y + text_box.height * 1.3))
        screen.blit(font_info.render("only letters, numbers, dots, dashes", True, (150, 150, 150)),
                    (3.6 * width / 20, text_box.y + text_box.height * 1.7))
        #   cursor
        update_groups([cursor_group], screen)

        clock.tick(GameSetup.fps)
        pygame.display.flip()


def leaderboard_menu(screen, clock, cursor_group):
    width, height = screen.get_size()
    font_title = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.05 * width))  # loading font
    font_scores_title = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.018 * width))  # loading font
    font_scores = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.014 * width))  # loading font

    #   surface and background
    # surface
    surface = pygame.Surface(screen.get_size())  # creates a new surface of the same dimensions as screen
    surface = surface.convert_alpha()  # making surface transparent
    surface.fill((0, 0, 0, 80))  # fill the whole screen with black transparent color

    # background
    background = pygame.image.load("assets/images/Background.png")
    background = pygame.transform.scale(background, (width, height))
    background = pygame.Surface.convert(background)

    # text
    title, game_text = GameSetup.set_language("statistics")

    #   create button instances
    back_button = button.Button(16 * width / 20, 70 * height / 80, "assets/images/button_01.png",
                                "assets/images/button_02.png", 0.15, 0.05, 0.025, 'Back', screen,
                                "assets/sounds/button_click.mp3", 0.2)
    #   load the json file.
    highscores = load()
    while True:
        screen.blit(background, (0, 0))
        screen.blit(surface, (0, 0))
        #   text "Leaderboard"
        screen.blit(font_title.render(title, True, (230, 230, 230)), (3.6 * width / 20, 3.4 * height / 20))
        #   BUTTON
        if back_button.draw_button_and_text(screen):
            return True
        #   display the high-scores.
        screen.blit(font_scores_title.render(game_text[0], True, (230, 230, 230)), (3.6 * width / 20, 27 * height / 80))
        screen.blit(font_scores_title.render(game_text[1], True, (230, 230, 230)), (8 * width / 20, 27 * height / 80))
        screen.blit(font_scores_title.render(game_text[2], True, (230, 230, 230)), (11.8 * width / 20, 27 * height / 80))
        screen.blit(font_scores_title.render(game_text[3], True, (230, 230, 230)), (15 * width / 20, 27 * height / 80))
        y_position = list(range(32, 62, 3))  # the number of numbers here makes the number of names in the scoreboard
        for (hi_name, hi_score, hi_selected_ship, hi_date), y in zip(highscores, y_position):
            screen.blit(font_scores.render(f'{hi_name}', True, (160, 160, 160)), (3.6 * width / 20, y * height / 80))
            screen.blit(font_scores.render(f'{hi_score}', True, (160, 160, 160)), (8 * width / 20, y * height / 80))
            screen.blit(font_scores.render(f'{hi_selected_ship}', True, (160, 160, 160)), (11.8 * width / 20, y * height / 80))
            screen.blit(font_scores.render(f'{hi_date}', True, (160, 160, 160)), (15 * width / 20, y * height / 80))
        #   event handling
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # to cancel
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:  # to quit game
                quit()
        #   cursor
        update_groups([cursor_group], screen)

        clock.tick(GameSetup.fps)
        pygame.display.flip()


def main_menu(screen, clock, cursor_group):
    width, height = screen.get_size()
    font_title = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.05 * width))
    font_music = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.01 * width))

    #   surface and background
    # surface
    surface = pygame.Surface(screen.get_size())  # creates a new surface of the same dimensions as screen
    surface = surface.convert_alpha()  # making surface transparent
    surface.fill((0, 0, 0, 80))  # fill the whole screen with black transparent color

    # background
    background = pygame.image.load("assets/images/Background.png")
    background = pygame.transform.scale(background, (width, height))
    background = pygame.Surface.convert(background)

    # text
    title, game_text = GameSetup.set_language("main_menu")

    #   create button instances
    play_button = button.Button(3.6 * width / 20, 32 * height / 80, "assets/images/button_01.png",
                                "assets/images/button_02.png", 0.3, 0.05, 0.025, game_text[0], screen,
                                "assets/sounds/button_click.mp3", 0.2)
    scoreboard_button = button.Button(3.6 * width / 20, 41 * height / 80, "assets/images/button_01.png",
                                      "assets/images/button_02.png", 0.3, 0.05, 0.025, game_text[1], screen,
                                      "assets/sounds/button_click.mp3", 0.2)
    aboutgame_button = button.Button(3.6 * width / 20, 50 * height / 80, "assets/images/button_01.png",
                                     "assets/images/button_02.png", 0.3, 0.05, 0.025, game_text[2], screen,
                                     "assets/sounds/button_click.mp3", 0.2)
    quit_button = button.Button(3.6 * width / 20, 59 * height / 80, "assets/images/button_01.png",
                                "assets/images/button_02.png", 0.3, 0.05, 0.025, game_text[3], screen,
                                "assets/sounds/button_click.mp3", 0.2)
    settings_button = button.Button(149 * (width / 150), width - (149 * (width / 150)),
                                    "assets/images/settings_button1.png", "assets/images/settings_button2.png", 0.04,
                                    0.04, 0.01, '', screen, "assets/sounds/button_click.mp3", 0.2)
    while True:
        screen.blit(background, (0, 0))
        screen.blit(surface, (0, 0))

        #   text "Space shooter"            Pavel: Pozdeji by to místo toho možná chtělo nějakou grafickou náhradu
        screen.blit(font_title.render("Space shooter", True, (230, 230, 230)), (3.6 * width / 20, 3.4 * height / 20))
        #   text "Soundtrack: Karl Casey @ White Bat Audio"

        text = font_music.render(game_text[4], True, (150, 150, 150))
        text_width = text.get_width()  # width of text
        screen.blit(text, (width - text_width * 1.02, 19.5 * height / 20))

        #   BUTTON
        play_button.update_text(game_text[0])
        scoreboard_button.update_text(game_text[1])
        aboutgame_button.update_text(game_text[2])
        quit_button.update_text(game_text[3])

        if play_button.draw_button_and_text(screen):
            return
        if scoreboard_button.draw_button_and_text(screen):
            leaderboard_menu(screen, clock, cursor_group)
        if aboutgame_button.draw_button_and_text(screen):
            aboutgame_menu(screen, clock, cursor_group)
        if quit_button.draw_button_and_text(screen):
            quit()
        if settings_button.draw_image_topRight(screen):
            settings_menu(screen, clock, cursor_group, background, "main")
            title, game_text = GameSetup.set_language("main_menu")
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:  # to quit game
                quit()
            if event.type == pygame.QUIT:
                quit()
        #   cursor
        update_groups([cursor_group], screen)

        clock.tick(GameSetup.fps)
        pygame.display.flip()


def pause_menu(screen, clock, score, player, cursor, cursor_group, storage_items, installed_items):
    width, height = screen.get_size()
    font_title = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.05 * width))

    #   surface and background
    # surface
    surface = pygame.Surface(screen.get_size())  # creates a new surface of the same dimensions as screen
    surface = surface.convert_alpha()  # making surface transparent

    # background
    background_copy = screen.copy()
    surface.fill((0, 0, 0, 170))  # fill the whole screen with black transparent color

    # ship
    ship_surf = player.image_non_rot
    new_width = int(ship_surf.get_width() * 1.9)
    new_height = int(ship_surf.get_height() * 1.9)
    ship_surf = pygame.transform.scale(ship_surf, (new_width, new_height))
    ship_rect = ship_surf.get_rect(center=(1150, 500))
    ship_mask = pygame.mask.from_surface(ship_surf)
    ship_surf_transparent = ship_surf.copy()
    ship_surf_transparent.set_alpha(100)

    # settings
    settings_icon = pygame.image.load("assets/images/settings_icon_big.png").convert_alpha()
    new_width = int(settings_icon.get_width() * 0.7)
    new_height = int(settings_icon.get_height() * 0.7)
    settings_icon = pygame.transform.scale(settings_icon, (new_width, new_height))
    settings_rect = settings_icon.get_rect()
    settings_rect.centerx = ship_rect.centerx
    settings_rect.centery = ship_rect.centery + 50

    # mouse mask
    mouse_mask = pygame.mask.from_surface(pygame.Surface((10, 10)))

    # text
    title, game_text = GameSetup.set_language("pause")

    #   create button instances
    resume_button = button.Button(3.6 * width / 20, 32 * height / 80, "assets/images/button_01.png",
                                  "assets/images/button_02.png", 0.3, 0.05, 0.025, game_text[0], screen,
                                  "assets/sounds/button_click.mp3", 0.2)
    main_menu_button = button.Button(3.6 * width / 20, 41 * height / 80, "assets/images/button_01.png",
                                     "assets/images/button_02.png", 0.3, 0.05, 0.025, game_text[1], screen,
                                     "assets/sounds/button_click.mp3", 0.2)
    quit_button = button.Button(3.6 * width / 20, 50 * height / 80, "assets/images/button_01.png",
                                "assets/images/button_02.png", 0.3, 0.05, 0.025, game_text[2], screen,
                                "assets/sounds/button_click.mp3", 0.2)
    settings_button = button.Button(149 * (width / 150), width - (149 * (width / 150)),
                                    "assets/images/settings_button1.png", "assets/images/settings_button2.png", 0.04,
                                    0.04, 0.01, '', screen, "assets/sounds/button_click.mp3", 0.2)
    while True:
        # actual ship
        ship_surf = player.image_non_rot
        new_width = int(ship_surf.get_width() * 1.9)
        new_height = int(ship_surf.get_height() * 1.9)
        ship_surf = pygame.transform.scale(ship_surf, (new_width, new_height))
        ship_surf_transparent = ship_surf.copy()
        ship_surf_transparent.set_alpha(100)

        # render background
        screen.blit(background_copy, (0, 0))
        screen.blit(surface, (0, 0))

        # update buttons
        resume_button.update_text(game_text[0])
        main_menu_button.update_text(game_text[1])
        quit_button.update_text(game_text[2])

        # mouse
        mouse_pos = pygame.mouse.get_pos()

        if ship_mask.overlap(mouse_mask, (mouse_pos[0] - ship_rect.x, mouse_pos[1] - ship_rect.y)):
            over_ship = True
        else:
            over_ship = False
        if over_ship:
            screen.blit(ship_surf_transparent, ship_rect)
            screen.blit(settings_icon, settings_rect)
        else:
            screen.blit(ship_surf, ship_rect)

        #   text "Main Menu"
        screen.blit(font_title.render(title, True, (230, 230, 230)), (3.6 * width / 20, 3.4 * height / 20))
        #   BUTTON
        if resume_button.draw_button_and_text(screen):
            return False
        if main_menu_button.draw_button_and_text(screen):
            return True
        if quit_button.draw_button_and_text(screen):
            quit()
        if settings_button.draw_image_topRight(screen):
            settings_menu(screen, clock, cursor_group, background_copy, "pause")
            title, game_text = GameSetup.set_language("pause")

        #   closing pause  menu
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # to continue play
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:  # to quit game
                quit()
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # mouse click
                if over_ship:
                    upgrade_menu(screen, clock, player, cursor, cursor_group, storage_items, installed_items)
        #   score and cursor
        render_score(screen, score, 230, 230, 230)
        update_groups([cursor_group], screen)

        clock.tick(GameSetup.fps)
        pygame.display.flip()


def upgrade_menu(screen, clock, player, cursor, cursor_group, storage_items, installed_items):
    player.update_animation()
    width, height = screen.get_size()

    # background
    background = pygame.image.load("assets/images/Background.png").convert_alpha()
    background = pygame.transform.scale(background, (width, height))
    storage = pygame.image.load("assets/images/storage.png").convert_alpha()

    # storage background
    storage = pygame.transform.scale(storage, (width, height))

    # mouse mask
    mouse_mask = pygame.mask.from_surface(pygame.Surface((10, 10)))

    # bin
    thrash_bin = pygame.image.load("assets/images/thrash_bin.png").convert_alpha()
    thrash_bin_rect = thrash_bin.get_rect()
    thrash_bin_rect.center = (1400, 740)

    enlarged_thrash_bin_size = pygame.Vector2(thrash_bin.get_size()) * 1.3
    enlarged_thrash_bin_surf = pygame.transform.scale(thrash_bin, enlarged_thrash_bin_size)
    enlarged_thrash_bin_rect = enlarged_thrash_bin_surf.get_rect()
    enlarged_thrash_bin_rect.center = thrash_bin_rect.center
    thrash_bin_mask = pygame.mask.from_surface(thrash_bin)
    over_thrash_bin = False

    # description
    font_description = pygame.font.Font('assets/fonts/PublicPixel.ttf', 28)

    # modules
    module_white = pygame.image.load("assets/images/module_white.png").convert_alpha()
    module_black = pygame.image.load("assets/images/module_black.png").convert_alpha()

    # text
    game_text = None
    for language in GameSetup.languages:
        if language['language'] == GameSetup.language:
            game_text = language['text']['upgrade']['content']

    font_title = pygame.font.Font('assets/fonts/PublicPixel.ttf', 32)

    # ship parts
    ship_parts_images = {
        "weapons": [],
        "cooling": [],
        "shield": [],
        "repair_module": [],
        "booster": []
    }
    for module in ship_parts_images.keys():
        for i in range(3):
            ship_parts_images[module].append(pygame.image.load(f"assets/images/{module}{i}.png").convert_alpha())

    # picked mark
    picked_mark = pygame.image.load("assets/images/picked_mark.png").convert_alpha()
    picked_mark_active = 0

    # ship
    ship_surf = player.build_ship(player.type)
    pos = (440, 320)
    new_width = int(ship_surf.get_width() * 2.3)
    new_height = int(ship_surf.get_height() * 2.3)
    ship_surf = pygame.transform.scale(ship_surf, (new_width, new_height))
    ship_rect = ship_surf.get_rect(center=pos)
    ship_mask = pygame.mask.from_surface(ship_surf)
    over_ship = False
    ship_surf_transparent = ship_surf.copy()
    ship_surf_transparent.set_alpha(100)

    # settings
    controller_icon = pygame.image.load("assets/images/controller.png").convert_alpha()
    controller_rect = controller_icon.get_rect()
    controller_rect.centerx = ship_rect.centerx
    controller_rect.centery = ship_rect.centery + 50

    # create buttons
    x = 932
    y = 78
    storage_buttons = [(x, y), (x + 260, y), (x, y + 260), (x + 260, y + 260)]
    module_buttons = {
        "weapons": (90, 118, True),
        "cooling": (628, 118, True),
        "shield": (55, 392, True),
        "repair_module": (663, 392, True),
        "booster": (353, 590, True)
    }
    max_level = 3

    while True:
        # render background
        screen.blit(background, (0, 0))
        screen.blit(storage, (0, 0))
        if over_ship:
            screen.blit(ship_surf_transparent, ship_rect)
            screen.blit(controller_icon, controller_rect)
        else:
            screen.blit(ship_surf, ship_rect)
        if over_thrash_bin:
            screen.blit(enlarged_thrash_bin_surf, enlarged_thrash_bin_rect)
        else:
            screen.blit(thrash_bin, thrash_bin_rect)

        description = None
        max_level_reached = False
        item_stat_color = 'white'
        for module, level in player.ship_parts.items():
            if 0 <= picked_mark_active < len(storage_items):
                if module == storage_items[picked_mark_active].upgrade_type:
                    if module == 'weapons':
                        current_dmg = player.proj_dmg_array[level]
                        current_fire_rate = player.fire_rate_array[level]
                        current_overheat = player.overheat_array[level]

                        if storage_items[picked_mark_active].upgradable:
                            if level + 1 > max_level:
                                max_level_reached = True
                                item_dmg = None
                                item_fire_rate = None
                                item_overheat = None
                            else:
                                item_dmg = player.proj_dmg_array[level + 1]
                                item_fire_rate = player.fire_rate_array[level + 1]
                                item_overheat = player.overheat_array[level + 1]
                        else:
                            item_dmg = player.proj_dmg_array[storage_items[picked_mark_active].level]
                            item_fire_rate = player.fire_rate_array[storage_items[picked_mark_active].level]
                            item_overheat = player.overheat_array[storage_items[picked_mark_active].level]

                        description = {'DMG:': (current_dmg, item_dmg),
                                       'Fire rate:': (current_fire_rate, item_fire_rate),
                                       'Overheat:': (current_overheat, item_overheat)}

                    elif module == 'cooling':
                        current_cooling = player.cooling_array[level]

                        if storage_items[picked_mark_active].upgradable:
                            if level + 1 > max_level:
                                max_level_reached = True
                                item_cooling = None
                            else:
                                item_cooling = player.cooling_array[level + 1]
                        else:
                            item_cooling = player.cooling_array[storage_items[picked_mark_active].level]

                        description = {'Cooling:': (current_cooling, item_cooling)}

                    elif module == 'repair_module':
                        current_regeneration = player.regeneration_array[level]

                        if storage_items[picked_mark_active].upgradable:
                            if level + 1 > max_level:
                                max_level_reached = True
                                item_regeneration = None
                            else:
                                item_regeneration = player.regeneration_array[level + 1]
                        else:
                            item_regeneration = player.regeneration_array[storage_items[picked_mark_active].level]

                        description = {'Regeneration:': (current_regeneration, item_regeneration)}

                    elif module == 'shield':
                        current_max_hp = player.max_hp_array[level]
                        current_collision_dmg = player.dmg_array[level]

                        if storage_items[picked_mark_active].upgradable:
                            if level + 1 > max_level:
                                max_level_reached = True
                                item_max_hp = None
                                item_collision_dmg = None
                            else:
                                item_max_hp = player.max_hp_array[level + 1]
                                item_collision_dmg = player.dmg_array[level + 1]
                        else:
                            item_max_hp = player.max_hp_array[storage_items[picked_mark_active].level]
                            item_collision_dmg = player.dmg_array[storage_items[picked_mark_active].level]

                        description = {'Max HP:': (current_max_hp, item_max_hp),
                                       'Collision DMG:': (current_collision_dmg, item_collision_dmg)}

                    elif module == 'booster':
                        current_acceleration = player.acceleration_array[level]

                        if storage_items[picked_mark_active].upgradable:
                            if level + 1 > max_level:
                                max_level_reached = True
                                item_acceleration = None
                            else:
                                item_acceleration = player.acceleration_array[level + 1]
                        else:
                            item_acceleration = player.acceleration_array[storage_items[picked_mark_active].level]

                        description = {'Acceleration:': (current_acceleration, item_acceleration)}
        if description:
            for i, (stat_name, (current_stat, item_stat)) in enumerate(description.items()):
                screen.blit(font_description.render(stat_name, True, 'white'), (660, 650 + i * 60))
                if max_level_reached:
                    screen.blit(font_description.render(str(current_stat), True, 'white'), (1050, 650 + i * 60))
                else:
                    screen.blit(font_description.render(str(current_stat) + ' → ', True, 'white'), (1050, 650 + i * 60))
                    width = font_description.render(str(current_stat) + ' → ', True, 'white').get_width()
                    if current_stat > item_stat:
                        item_stat_color = 'red'
                    elif current_stat < item_stat:
                        item_stat_color = 'green'
                    screen.blit(font_description.render(str(item_stat), True, item_stat_color),
                                (1050 + width, 650 + i * 60))

        # rendering storage items
        for i, item in enumerate(storage_items):
            # calculating centers of rects
            storage_button_x = storage_buttons[i][0] + 132
            storage_button_y = storage_buttons[i][1] + 130

            item_rect = item.unscaled_image.get_rect()
            item_x = storage_button_x - item_rect.width // 2
            item_y = storage_button_y - item_rect.height // 2
            screen.blit(item.unscaled_image, (item_x, item_y))

        # rendering modules
        for i, (module, (x, y, active)) in enumerate(module_buttons.items()):
            module_rect = module_white.get_rect()
            module_rect.x = x
            module_rect.y = y
            if active:
                screen.blit(module_white, module_rect)
            else:
                screen.blit(module_black, module_rect)

            text = font_title.render(game_text[i], True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.centerx = module_rect.centerx
            text_rect.y = module_rect.y + 180
            screen.blit(text, text_rect)

        # rendering installed items
        for module, i in player.ship_parts.items():
            # calculating centers of module rects
            if i > 0:
                module_button_x, module_button_y, active = module_buttons[module]
                module_button_x_center = module_button_x + 93
                module_button_y_center = module_button_y + 90

                item_rect = ship_parts_images[module][player.ship_parts[module] - 1].get_rect()
                item_x = module_button_x_center - item_rect.width // 2
                item_y = module_button_y_center - item_rect.height // 2
                screen.blit(ship_parts_images[module][player.ship_parts[module] - 1], (item_x, item_y))

        # rendering picked mark
        if picked_mark_active >= 0:
            # calculating centers of storage button rects
            storage_button_x = storage_buttons[picked_mark_active][0] + 132
            storage_button_y = storage_buttons[picked_mark_active][1] + 130

            picked_mark_rect = picked_mark.get_rect()
            picked_mark_x = storage_button_x - picked_mark_rect.width // 2
            picked_mark_y = storage_button_y - picked_mark_rect.height // 2
            screen.blit(picked_mark, (picked_mark_x, picked_mark_y))

        # searching if the item type fits the part of the ship, the ones that doesn't fit are unactive
        for module, (x, y, active) in module_buttons.items():
            if 0 <= picked_mark_active < len(storage_items):
                if module == storage_items[picked_mark_active].upgrade_type:
                    module_buttons[module] = (x, y, True)
                else:
                    module_buttons[module] = (x, y, False)
            else:
                module_buttons[module] = (x, y, True)

        mouse_pos = pygame.mouse.get_pos()
        if thrash_bin_mask.overlap(mouse_mask, (mouse_pos[0] - thrash_bin_rect.x, mouse_pos[1] - thrash_bin_rect.y)):
            over_thrash_bin = True
        else:
            over_thrash_bin = False
        if ship_mask.overlap(mouse_mask, (mouse_pos[0] - ship_rect.x, mouse_pos[1] - ship_rect.y)):
            over_ship = True
        else:
            over_ship = False

        # closing upgrade menu
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # to continue play
                player.image_non_rot_orig = player.build_ship(player.type)
                player.image_non_rot_orig = pygame.transform.scale_by(player.image_non_rot_orig, player.img_scale_ratio)
                player.image_non_rot_orig = player.scale_image(player.image_non_rot_orig)
                player.image_non_rot = player.image_non_rot_orig
                player.image = player.image_non_rot
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q or event.type == pygame.QUIT:  # to quit game
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # mouse click
                if over_thrash_bin and picked_mark_active < len(storage_items):
                    storage_items.pop(picked_mark_active)
                if over_ship:
                    menu_cockpit(screen, clock, player, cursor, cursor_group)  # entering cockpit menu

                # collision with storage rects
                for i, (x, y) in enumerate(storage_buttons):
                    rect = pygame.Rect(x, y, 260, 260)
                    if rect.collidepoint(mouse_pos):
                        picked_mark_active = i
                        break

                # collision with module rects
                for module, (x, y, active) in module_buttons.items():
                    rect = pygame.Rect(x, y, 260, 260)
                    if rect.collidepoint(mouse_pos):
                        if picked_mark_active < len(storage_items):
                            if storage_items[picked_mark_active].upgradable:
                                if installed_items[module]:
                                    if player.ship_parts[module] + 1 <= max_level:
                                        installed_items[module].level_up()
                                        player.ship_parts[module] += 1
                                        storage_items.pop(picked_mark_active)
                                    else:
                                        storage_items.append(installed_items[module])
                                        installed_items[module] = None
                                        player.ship_parts[module] = 0
                                else:
                                    if module == storage_items[picked_mark_active].upgrade_type:
                                        player.ship_parts[module] += 1
                                        installed_items[module] = ShipUpgrade((0, 0), module, False)
                                        storage_items.pop(picked_mark_active)
                            else:
                                if installed_items[module]:
                                    storage_items.append(installed_items[module])
                                    installed_items[module] = None
                                    player.ship_parts[module] = 0
                                else:
                                    if picked_mark_active < len(storage_items):
                                        if module == storage_items[picked_mark_active].upgrade_type:
                                            installed_items[module] = storage_items[picked_mark_active]
                                            player.ship_parts[module] = installed_items[module].level
                                            storage_items.pop(picked_mark_active)
                        else:
                            if installed_items[module]:
                                storage_items.append(installed_items[module])
                                installed_items[module] = None
                                player.ship_parts[module] = 0

                player.image_non_rot_orig = player.build_ship(player.type)
                player.image_non_rot_orig = pygame.transform.scale_by(player.image_non_rot_orig, player.img_scale_ratio)
                player.image_non_rot_orig = player.scale_image(player.image_non_rot_orig)
                player.image_non_rot = player.image_non_rot_orig
                player.image = player.image_non_rot

                player.update_animation()
                ship_surf = player.build_ship(player.type)
                ship_surf = pygame.transform.scale(ship_surf, (new_width, new_height))
        player.update_parameters()

        # cursor
        update_groups([cursor_group], screen)

        clock.tick(GameSetup.fps)
        pygame.display.flip()


def menu_cockpit(screen, clock, player, cursor, cursor_group):
    width, height = screen.get_size()
    in_minigame = False

    # hp
    hp = []
    for i in range(4):
        img = pygame.image.load(f"assets/images/cockpit/hp{i}.png").convert_alpha()
        hp.append(img)

    # background
    background_image = Background("cockpit", 5, (30, 100))
    background_group = pygame.sprite.Group()
    background_group.add(background_image)

    # button
    play_button = button.Button(650, 330, "assets/images/cockpit/button_01.png",
                                "assets/images/cockpit/button_02.png", 0.15, 0.05,
                                0.021, '', screen, "assets/sounds/button_click.mp3",
                                0.3)

    (mini_enemy_group, mini_spawner_group, mini_item_group, mini_player_projectile_group,
     mini_enemy_projectile_group, mini_explosion_group, mini_player, mini_player_group) = set_minigame()

    cursor.set_cursor()

    while True:

        # closing upgrade menu
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # to continue play
                if in_minigame:
                    in_minigame = False
                    cursor.set_cursor()
                    (mini_enemy_group, mini_spawner_group, mini_item_group, mini_player_projectile_group,
                     mini_enemy_projectile_group, mini_explosion_group, mini_player, mini_player_group) = set_minigame()
                else:
                    return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q or event.type == pygame.QUIT:  # to quit game
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # mouse click
                pass

        if in_minigame:
            # updating groups
            update_groups(
                [background_group, mini_player_projectile_group, mini_enemy_projectile_group, mini_enemy_group,
                 mini_player_group, mini_spawner_group, mini_explosion_group], screen)

            screen.blit(hp[int(mini_player.hp)], (520, 500))

            # updating cursor
            update_groups([cursor_group], screen)

            handle_collisions(mini_item_group, mini_player_group, False, mini_enemy_group, False, mini_explosion_group)
            handle_collisions(mini_item_group, mini_player_projectile_group, True, mini_enemy_group, False,
                              mini_explosion_group)
            handle_collisions(mini_item_group, mini_enemy_projectile_group, True, mini_player_group, False,
                              mini_explosion_group)
            handle_collisions(mini_item_group, mini_player_projectile_group, True, mini_enemy_projectile_group, True,
                              mini_explosion_group)

            cursor.check_cursor()

            # FPS lock and adding time
            time_diff = clock.tick(GameSetup.fps) / 1000
            update_time([mini_player_group, mini_enemy_group, mini_item_group, mini_spawner_group], time_diff)

            if not mini_player_group and not mini_explosion_group:
                #   death_menu
                in_minigame = False
                cursor.set_cursor()
                (mini_enemy_group, mini_spawner_group, mini_item_group, mini_player_projectile_group,
                 mini_enemy_projectile_group, mini_explosion_group, mini_player, mini_player_group) = set_minigame()
        else:
            screen.blit(mini_player.image, mini_player.rect)
            update_groups([background_group], screen)
            screen.blit(hp[3], (520, 500))
            update_groups([cursor_group], screen)
            if play_button.draw_button_and_text(screen):
                in_minigame = True

        pygame.display.flip()
        clock.tick(GameSetup.fps)


def set_minigame():
    # groups
    mini_enemy_group = pygame.sprite.Group()
    mini_spawner_group = pygame.sprite.Group()
    mini_item_group = pygame.sprite.Group()
    mini_player_projectile_group = pygame.sprite.Group()
    mini_enemy_projectile_group = pygame.sprite.Group()
    mini_explosion_group = pygame.sprite.Group()
    mini_player_group = pygame.sprite.Group()

    # player
    mini_player = MiniPlayer(mini_player_projectile_group)
    mini_player_group.add(mini_player)

    mini_zarovka_spawner = EnemySpawner(mini_enemy_group, "minizarovka", 3, mini_player)
    mini_spawner_group.add(mini_zarovka_spawner)

    return (mini_enemy_group, mini_spawner_group, mini_item_group, mini_player_projectile_group,
            mini_enemy_projectile_group, mini_explosion_group, mini_player, mini_player_group)


def ship_menu(screen, clock, cursor_group):
    width, height = screen.get_size()

    #   surface and background
    # surface
    surface = pygame.Surface(screen.get_size())  # creates a new surface of the same dimensions as screen
    surface = surface.convert_alpha()  # making surface transparent
    surface.fill((0, 0, 0, 80))  # fill the whole screen with black transparent color

    # background
    background = pygame.image.load("assets/images/Background.png")
    background = pygame.transform.scale(background, (width, height))
    background = pygame.Surface.convert(background)

    # text
    title, game_text = GameSetup.set_language("ship_select")

    #   text
    font_title = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.05 * width))
    text = font_title.render(title, True, (230, 230, 230))
    text_rect = text.get_rect()
    text_rect.centerx = width / 2
    text_rect.y = 3.4 * height / 20

    #   create button instances
    Light_button = button.Button(2 * width / 8, 8 * height / 16, "assets/images/player_light/vlod_player_light.png",
                                 "assets/images/player_light/vlod_player_light.png",
                                 0.08, 0.1, 0.02, 'Light', screen, "assets/sounds/game_start.mp3", 0.3)
    Mid_button = button.Button(4 * width / 8, 8 * height / 16, "assets/images/player_mid/vlod_player_mid.png",
                               "assets/images/player_mid/vlod_player_mid.png",
                               0.09, 0.1, 0.02, 'Mid', screen, "assets/sounds/game_start.mp3", 0.2)
    Tank_button = button.Button(6 * width / 8, 8 * height / 16, "assets/images/player_tank/vlod_player_tank.png",
                                "assets/images/player_tank/vlod_player_tank.png",
                                0.08, 0.1, 0.02, 'Tank', screen, "assets/sounds/game_start.mp3", 0.2)
    while True:
        screen.blit(background, (0, 0))
        screen.blit(surface, (0, 0))
        #   text "Ship selection"
        screen.blit(text, text_rect)
        #   text of ships properties
        #   button
        if Light_button.draw_image_in_center(screen, game_text):
            return 1
        if Mid_button.draw_image_in_center(screen, game_text):
            return 2
        if Tank_button.draw_image_in_center(screen, game_text):
            return 3
        #   Event handling
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:  # to quit game
                quit()
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 0
        #   cursor
        update_groups([cursor_group], screen)

        clock.tick(GameSetup.fps)
        pygame.display.flip()


def death_menu(screen, clock, cursor_group, score, ship_number):
    width, height = screen.get_size()
    font_title = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.05 * width))
    font_score = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.025 * width))

    #   surface and background
    # surface
    surface = pygame.Surface(screen.get_size())  # creates a new surface of the same dimensions as screen
    surface = surface.convert_alpha()  # making surface transparent
    surface.fill((0, 0, 0, 230))  # fill the whole screen with black transparent color

    # background
    background = pygame.image.load("assets/images/Background.png")
    background = pygame.transform.scale(background, (width, height))
    background = pygame.Surface.convert(background)

    # text
    title, game_text = GameSetup.set_language("game_over")

    #   create button instances
    save_name_button = button.Button(3.6 * width / 20, 32 * height / 80, "assets/images/button_01.png",
                                     "assets/images/button_02.png", 0.35, 0.05, 0.025, game_text[1], screen,
                                     "assets/sounds/button_click.mp3", 0.3)
    restart_button = button.Button(3.6 * width / 20, 41 * height / 80, "assets/images/button_01.png",
                                   "assets/images/button_02.png", 0.35, 0.05, 0.025, game_text[2], screen,
                                   "assets/sounds/button_click.mp3", 0.3)
    main_menu_button = button.Button(3.6 * width / 20, 50 * height / 80, "assets/images/button_01.png",
                                     "assets/images/button_02.png", 0.35, 0.05, 0.025, game_text[3], screen,
                                     "assets/sounds/button_click.mp3", 0.2)
    quit_button = button.Button(3.6 * width / 20, 59 * height / 80, "assets/images/button_01.png",
                                "assets/images/button_02.png", 0.35, 0.05, 0.025, game_text[4], screen,
                                "assets/sounds/button_click.mp3", 0.2)
    #   sound
    sound = pygame.mixer.Sound("assets/sounds/game_over.mp3")  # Load sound file
    sound.set_volume(0.6 * GameSetup.effects_volume)
    pygame.mixer.find_channel(False).play(sound)
    #   a variable that makes it possible to make the save name button disappear after saving a name
    save_name_clicked = False
    while True:
        screen.blit(background, (0, 0))
        screen.blit(surface, (0, 0))
        #   text "Game over" and "score"
        screen.blit(font_title.render(title, True, (230, 230, 230)), (3.6 * width / 20, 3.4 * height / 20))
        score_text = game_text[0] + str(score)
        screen.blit(font_score.render(score_text, True, (230, 230, 230)), (3.6 * width / 20, 5.7 * height / 20))
        #   button
        if not save_name_clicked:
            if save_name_button.draw_button_and_text(screen):
                save_name_clicked = save_name_menu(screen, clock, cursor_group, score, ship_number)
                # save_name_clicked = True
        if restart_button.draw_button_and_text(screen):
            return False
        if main_menu_button.draw_button_and_text(screen):
            return True
        if quit_button.draw_button_and_text(screen):
            quit()
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:  # to quit game
                quit()
            if event.type == pygame.QUIT:
                quit()
        #   cursor
        update_groups([cursor_group], screen)

        clock.tick(GameSetup.fps)
        pygame.display.flip()


def aboutgame_menu(screen, clock, cursor_group):
    width, height = screen.get_size()
    #   variable for scroll
    record = True
    y_scroll = 0

    # mouse mask
    mouse_mask = pygame.mask.from_surface(pygame.Surface((10, 10)))

    #   text
    # variables for text
    spaceBetween = 0.009 * width
    textAlignLeft = 0
    textAlignRight = 1
    textAlignCenter = 2
    textAlignBlock = 3

    # ship images
    vlod5L = pygame.image.load("assets/images/player_light/vlod_player_light.png").convert_alpha()
    vlod5L = pygame.transform.scale(vlod5L, (int(width * 0.08), int(width * 0.09)))  # transforming image
    vlod5L_pos = vlod5L.get_rect().center
    new_width = int(vlod5L.get_width() * 1.4)
    new_height = int(vlod5L.get_height() * 1.4)
    vlod5L_rect = vlod5L.get_rect(center=vlod5L_pos)
    enlarged_vlod5L = pygame.transform.scale(vlod5L, (new_width, new_height))
    enlarged_vlod5L_rect = enlarged_vlod5L.get_rect()
    enlarged_vlod5L_rect.center = vlod5L_rect.center
    vlod5L_mask = pygame.mask.from_surface(vlod5L)
    over_vlod5L = False

    vlod5 = pygame.image.load("assets/images/player_mid/vlod_player_mid.png").convert_alpha()
    vlod5 = pygame.transform.scale(vlod5, (int(width * 0.11), int(width * 0.12)))  # transforming image
    vlod5_pos = vlod5.get_rect().center
    new_width = int(vlod5.get_width() * 1.4)
    new_height = int(vlod5.get_height() * 1.4)
    vlod5_rect = vlod5.get_rect(center=vlod5_pos)
    enlarged_vlod5 = pygame.transform.scale(vlod5, (new_width, new_height))
    enlarged_vlod5_rect = enlarged_vlod5.get_rect()
    enlarged_vlod5_rect.center = vlod5_rect.center
    vlod5_mask = pygame.mask.from_surface(vlod5)
    over_vlod5 = False

    vlod5T = pygame.image.load("assets/images/player_tank/vlod_player_tank.png").convert_alpha()
    vlod5T = pygame.transform.scale(vlod5T, (int(width * 0.1), int(width * 0.12)))  # transforming image
    vlod5T_pos = vlod5T.get_rect().center
    new_width = int(vlod5T.get_width() * 1.4)
    new_height = int(vlod5T.get_height() * 1.4)
    vlod5T_rect = vlod5T.get_rect(center=vlod5T_pos)
    enlarged_vlod5T = pygame.transform.scale(vlod5T, (new_width, new_height))
    enlarged_vlod5T_rect = enlarged_vlod5T.get_rect()
    enlarged_vlod5T_rect.center = vlod5T_rect.center
    vlod5T_mask = pygame.mask.from_surface(vlod5T)
    over_vlod5T = False

    # fonts for text
    font_title = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.05 * width))  # loading font
    title_color = (230, 230, 230)
    font_subtitle = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.02 * width))  # loading font
    subtitle_height = font_subtitle.size("Tq")[1]  # height of font
    font_text = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.01 * width))  # loading font
    text_height = font_text.size("Tq")[1]  # height of font
    text_color = (180, 180, 180)
    font_name = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.012 * width))  # loading font
    name_color = (200, 200, 200)

    #   surface and background
    # surface
    surface = pygame.Surface(screen.get_size())  # creates a new surface of the same dimensions as screen
    surface = surface.convert_alpha()  # making surface transparent
    surface.fill((0, 0, 0, 80))  # fill the whole screen with black transparent color

    # background
    background = pygame.image.load("assets/images/Background.png")
    background = pygame.transform.scale(background, (width, height))
    background = pygame.Surface.convert(background)

    # text
    title, game_text = GameSetup.set_language("about_game")

    #   create button instances
    back_button = button.Button(16.5 * width / 20, 70 * height / 80, "assets/images/button_01.png",
                                "assets/images/button_02.png", 0.15, 0.05, 0.025, game_text[33], screen,
                                "assets/sounds/button_click.mp3", 0.2)
    while True:
        screen.blit(background, (0, 0))
        screen.blit(surface, (0, 0))
        #   text "About game"
        screen.blit(font_title.render(title, True, (230, 230, 230)),
                    (3.6 * width / 20, (3.4 * height / 20) + y_scroll))

        mouse_pos = pygame.mouse.get_pos()

        #   BUTTON
        if back_button.draw_button_and_text(screen):
            return True
        #   about game text
        # about game

        textRect = pygame.Rect(3.6 * width / 20, (27 * height / 80) + y_scroll, 12 * width / 20,
                               50)  # x-axis, y-axis, size on x-axis, size on y-axis
        lowest_value = drawText.drawText(screen, game_text[0], text_color, textRect, font_text, textAlignLeft, True, None)
        # why was created
        textRect = pygame.Rect(3.6 * width / 20, lowest_value + spaceBetween * 2, 12 * width / 20,
                               50)  # x-axis, y-axis, size on x-axis, size on y-axis
        lowest_value = drawText.drawText(screen, game_text[1], text_color, textRect, font_text, textAlignLeft, True, None)
        # development team
        screen.blit(font_subtitle.render(game_text[2], True, title_color),
                    (3.6 * width / 20, lowest_value + spaceBetween * 4))
        lowest_value = lowest_value + spaceBetween * 4 + subtitle_height
        screen.blit(font_text.render(game_text[3], True, text_color),
                    (3.6 * width / 20, lowest_value + spaceBetween * 2))
        screen.blit(font_text.render(game_text[4], True, text_color),
                    (8 * width / 20, lowest_value + spaceBetween * 2))
        lowest_value = lowest_value + spaceBetween * 2 + text_height
        screen.blit(font_text.render(game_text[5], True, text_color),
                    (3.6 * width / 20, lowest_value + spaceBetween))
        screen.blit(font_text.render(game_text[6], True, text_color), (8 * width / 20, lowest_value + spaceBetween))
        lowest_value = lowest_value + spaceBetween + text_height
        # controls
        screen.blit(font_subtitle.render(game_text[7], True, title_color),
                    (3.6 * width / 20, lowest_value + spaceBetween * 4))
        lowest_value = lowest_value + spaceBetween * 4 + subtitle_height
        screen.blit(font_text.render(game_text[8], True, text_color),
                    (3.6 * width / 20, lowest_value + spaceBetween * 2))
        screen.blit(font_text.render(game_text[9], True, text_color),
                    (3.6 * width / 20, lowest_value + spaceBetween * 3 + text_height))
        screen.blit(font_text.render(game_text[10], True, text_color),
                    (3.6 * width / 20, lowest_value + spaceBetween * 4 + text_height * 2))
        screen.blit(font_text.render(game_text[11], True, text_color),
                    (3.6 * width / 20, lowest_value + spaceBetween * 5 + text_height * 3))
        screen.blit(font_text.render(game_text[12], True, text_color),
                    (3.6 * width / 20, lowest_value + spaceBetween * 6 + text_height * 4))
        lowest_value = lowest_value + spaceBetween * 6 + text_height * 5
        #   ships
        screen.blit(font_subtitle.render(game_text[13], True, title_color),
                    (3.6 * width / 20, lowest_value + spaceBetween * 4))
        lowest_value = lowest_value + spaceBetween * 4 + subtitle_height

        # checking if mouse is over image
        if vlod5L_mask.overlap(mouse_mask, (mouse_pos[0] - ((5 * width / 20) + vlod5L_rect.x - vlod5L_rect.width / 2),
                                            mouse_pos[1] - (
                                                    lowest_value + 7 * spaceBetween + 4.5 * text_height + vlod5L_rect.y - vlod5L_rect.height / 2))):
            over_vlod5L = True
        else:
            over_vlod5L = False

        # ship number 1
        if over_vlod5L:
            screen.blit(enlarged_vlod5L, ((5 * width / 20) + enlarged_vlod5L_rect.x - vlod5L_rect.width / 2,
                                          lowest_value + 7 * spaceBetween + 4.5 * text_height + vlod5L_rect.y - enlarged_vlod5L_rect.height / 2))
        else:
            screen.blit(vlod5L, ((5 * width / 20) + vlod5L_rect.x - vlod5L_rect.width / 2,
                                 lowest_value + 7 * spaceBetween + 4.5 * text_height + vlod5L_rect.y - vlod5L_rect.height / 2))
        # load info about ship from json
        with open("playerships/playerparams.json", "r") as param_file:
            enemy_param = json.load(param_file)
        Ship_param = enemy_param[0]

        # write info about ship

        if over_vlod5L:
            text = font_name.render("LIGHT", True, name_color)
            screen.blit(text, ((5 * width / 20) - text.get_width() / 2, lowest_value + 2 * spaceBetween))
            screen.blit(font_text.render(f"{game_text[14]}{Ship_param['hp']}", True, text_color),
                        (7.5 * width / 20, lowest_value + 4 * spaceBetween + text_height))
            screen.blit(font_text.render(f"{game_text[15]}{Ship_param['proj_dmg']}", True, text_color),
                        (7.5 * width / 20, lowest_value + 5 * spaceBetween + 2 * text_height))
            screen.blit(font_text.render(f"{game_text[16]}{Ship_param['fire_rate']}", True, text_color),
                        (7.5 * width / 20, lowest_value + 6 * spaceBetween + 3 * text_height))
            textAcc = font_text.render(f"{game_text[17]}{Ship_param['acceleration']}", True, text_color)
            textAcc_width = textAcc.get_width()  # getting width of text
            screen.blit(textAcc, (7.5 * width / 20, lowest_value + 7 * spaceBetween + 4 * text_height))
            screen.blit(font_text.render(f"{game_text[18]}{Ship_param['max_velocity']}", True, text_color),
                        (7.5 * width / 20, lowest_value + 8 * spaceBetween + 5 * text_height))
        else:

            text = font_name.render("LIGHT", True, name_color)
            screen.blit(text, ((5 * width / 20) - text.get_width() / 2, lowest_value + 2 * spaceBetween))
            screen.blit(font_text.render(f"{game_text[14]}{Ship_param['hp'][0]}", True, text_color),
                        (7.5 * width / 20, lowest_value + 4 * spaceBetween + text_height))
            screen.blit(font_text.render(f"{game_text[15]}{Ship_param['proj_dmg'][0]}", True, text_color),
                        (7.5 * width / 20, lowest_value + 5 * spaceBetween + 2 * text_height))
            screen.blit(font_text.render(f"{game_text[16]}{Ship_param['fire_rate'][0]}", True, text_color),
                        (7.5 * width / 20, lowest_value + 6 * spaceBetween + 3 * text_height))
            textAcc = font_text.render(f"{game_text[17]}{Ship_param['acceleration'][0]}", True, text_color)
            textAcc_width = textAcc.get_width() + 100  # getting width of text
            screen.blit(textAcc, (7.5 * width / 20, lowest_value + 7 * spaceBetween + 4 * text_height))
            screen.blit(font_text.render(f"{game_text[18]}{Ship_param['max_velocity']}", True, text_color),
                        (7.5 * width / 20, lowest_value + 8 * spaceBetween + 5 * text_height))
        #   skills
        # skill Q
        text_skill_01 = font_text.render(game_text[19], True, text_color)
        text_skill_01_width = text_skill_01.get_width()  # getting width of text
        screen.blit(text_skill_01,
                    (((7.5 * width / 20) + textAcc_width * 1.25), lowest_value + 4 * spaceBetween + text_height))
        text_skill_02 = font_text.render(game_text[21], True, text_color)
        text_skill_02_width = text_skill_02.get_width()  # getting width of text
        text_skill_02_height = text_skill_02.get_height()  # getting height of text
        screen.blit(text_skill_02, (((7.5 * width / 20) + textAcc_width * 1.25 + text_skill_01_width),
                                    lowest_value + 4 * spaceBetween + text_height))
        image_Q = pygame.image.load("assets/images/skills_aboutGame/Q_dash_aboutGame.png").convert_alpha()  # load image
        image_Q = pygame.transform.scale(image_Q, (int(width * 0.03), int(width * 0.03)))  # transforming image
        image_width = image_Q.get_width()  # getting width of image
        screen.blit(image_Q, (
            (((
                      7.5 * width / 20) + textAcc_width * 1.25 + text_skill_01_width + text_skill_02_width / 2) - image_width / 2),
            lowest_value + 4 * spaceBetween + text_height + text_skill_02_height * 1.5))
        # skill E
        text_skill_01 = font_text.render(game_text[20], True, text_color)
        text_skill_01_width = text_skill_01.get_width()  # getting width of text
        screen.blit(text_skill_01,
                    (((7.5 * width / 20) + textAcc_width * 1.25), lowest_value + 7 * spaceBetween + 4 * text_height))
        text_skill_02 = font_text.render(game_text[22], True, text_color)
        text_skill_02_width = text_skill_02.get_width()  # getting width of text
        text_skill_02_height = text_skill_02.get_height()  # getting height of text
        screen.blit(text_skill_02, (((7.5 * width / 20) + textAcc_width * 1.25 + text_skill_01_width),
                                    lowest_value + 7 * spaceBetween + 4 * text_height))
        image_Q = pygame.image.load(
            "assets/images/skills_aboutGame/E_shield_aboutGame.png").convert_alpha()  # load image
        image_Q = pygame.transform.scale(image_Q, (int(width * 0.03), int(width * 0.03)))  # transforming image
        image_width = image_Q.get_width()  # getting width of image
        screen.blit(image_Q, (
            (((
                      7.5 * width / 20) + textAcc_width * 1.25 + text_skill_01_width + text_skill_02_width / 2) - image_width / 2),
            lowest_value + 7 * spaceBetween + 4 * text_height + text_skill_02_height * 1.5))
        #   new lowest value
        lowest_value = lowest_value + 10 * spaceBetween + 7 * text_height + 4 * spaceBetween

        # ship number 2

        # checking if mouse is over image
        if vlod5_mask.overlap(mouse_mask, (mouse_pos[0] - ((5 * width / 20) + vlod5_rect.x - vlod5_rect.width / 2),
                                           mouse_pos[1] - (
                                                   lowest_value + 7 * spaceBetween + 4.5 * text_height + vlod5_rect.y - vlod5_rect.height / 2))):
            over_vlod5 = True
        else:
            over_vlod5 = False

        # write image
        if over_vlod5:
            screen.blit(enlarged_vlod5, ((5 * width / 20) + enlarged_vlod5_rect.x - vlod5_rect.width / 2,
                                         lowest_value + 7 * spaceBetween + 4.5 * text_height + vlod5_rect.y - enlarged_vlod5_rect.height / 2))
        else:
            screen.blit(vlod5, ((5 * width / 20) + vlod5_rect.x - vlod5_rect.width / 2,
                                lowest_value + 7 * spaceBetween + 4.5 * text_height + vlod5_rect.y - vlod5_rect.height / 2))

        with open("playerships/playerparams.json", "r") as param_file:
            enemy_param = json.load(param_file)
        Ship_param = enemy_param[1]
        # write info about ship
        text = font_name.render("MID", True, name_color)

        if over_vlod5:
            screen.blit(text, ((5 * width / 20) - text.get_width() / 2, lowest_value + 2 * spaceBetween))
            screen.blit(font_text.render(f"{game_text[14]}{Ship_param['hp']}", True, text_color),
                        (7.5 * width / 20, lowest_value + 4 * spaceBetween + text_height))
            screen.blit(font_text.render(f"{game_text[15]}{Ship_param['proj_dmg']}", True, text_color),
                        (7.5 * width / 20, lowest_value + 5 * spaceBetween + 2 * text_height))
            screen.blit(font_text.render(f"{game_text[16]}{Ship_param['fire_rate']}", True, text_color),
                        (7.5 * width / 20, lowest_value + 6 * spaceBetween + 3 * text_height))
            textAcc = font_text.render(f"{game_text[17]}{Ship_param['acceleration']}", True, text_color)
            textAcc_width = textAcc.get_width()  # getting width of text
            screen.blit(textAcc, (7.5 * width / 20, lowest_value + 7 * spaceBetween + 4 * text_height))
            screen.blit(font_text.render(f"{game_text[18]}{Ship_param['max_velocity']}", True, text_color),
                        (7.5 * width / 20, lowest_value + 8 * spaceBetween + 5 * text_height))
        else:
            screen.blit(text, ((5 * width / 20) - text.get_width() / 2, lowest_value + 2 * spaceBetween))
            screen.blit(font_text.render(f"{game_text[14]}{Ship_param['hp'][0]}", True, text_color),
                        (7.5 * width / 20, lowest_value + 4 * spaceBetween + text_height))
            screen.blit(font_text.render(f"{game_text[15]}{Ship_param['proj_dmg'][0]}", True, text_color),
                        (7.5 * width / 20, lowest_value + 5 * spaceBetween + 2 * text_height))
            screen.blit(font_text.render(f"{game_text[16]}{Ship_param['fire_rate'][0]}", True, text_color),
                        (7.5 * width / 20, lowest_value + 6 * spaceBetween + 3 * text_height))
            textAcc = font_text.render(f"{game_text[17]}{Ship_param['acceleration'][0]}", True, text_color)
            textAcc_width = textAcc.get_width() + 100  # getting width of text
            screen.blit(textAcc, (7.5 * width / 20, lowest_value + 7 * spaceBetween + 4 * text_height))
            screen.blit(font_text.render(f"{game_text[18]}{Ship_param['max_velocity']}", True, text_color),
                        (7.5 * width / 20, lowest_value + 8 * spaceBetween + 5 * text_height))
        #   skills
        # skill Q
        text_skill_01 = font_text.render(game_text[19], True, text_color)
        text_skill_01_width = text_skill_01.get_width()  # getting width of text
        screen.blit(text_skill_01,
                    (((7.5 * width / 20) + textAcc_width * 1.1), lowest_value + 4 * spaceBetween + text_height))
        text_skill_02 = font_text.render(game_text[23], True, text_color)
        text_skill_02_width = text_skill_02.get_width()  # getting width of text
        text_skill_02_height = text_skill_02.get_height()  # getting height of text
        screen.blit(text_skill_02, (((7.5 * width / 20) + textAcc_width * 1.1 + text_skill_01_width),
                                    lowest_value + 4 * spaceBetween + text_height))
        image_Q = pygame.image.load(
            "assets/images/skills_aboutGame/Q_rapidfire_aboutGame.png").convert_alpha()  # load image
        image_Q = pygame.transform.scale(image_Q, (int(width * 0.03), int(width * 0.03)))  # transforming image
        image_width = image_Q.get_width()  # getting width of image
        screen.blit(image_Q, (
            (((
                      7.5 * width / 20) + textAcc_width * 1.1 + text_skill_01_width + text_skill_02_width / 2) - image_width / 2),
            lowest_value + 4 * spaceBetween + text_height + text_skill_02_height * 1.5))
        # skill E
        text_skill_01 = font_text.render(game_text[20], True, text_color)
        text_skill_01_width = text_skill_01.get_width()  # getting width of text
        screen.blit(text_skill_01,
                    (((7.5 * width / 20) + textAcc_width * 1.1), lowest_value + 7 * spaceBetween + 4 * text_height))
        text_skill_02 = font_text.render(game_text[24], True, text_color)
        text_skill_02_width = text_skill_02.get_width()  # getting width of text
        text_skill_02_height = text_skill_02.get_height()  # getting height of text
        screen.blit(text_skill_02, (((7.5 * width / 20) + textAcc_width * 1.1 + text_skill_01_width),
                                    lowest_value + 7 * spaceBetween + 4 * text_height))
        image_Q = pygame.image.load(
            "assets/images/skills_aboutGame/E_blastshoot_aboutGame.png").convert_alpha()  # load image
        image_Q = pygame.transform.scale(image_Q, (int(width * 0.03), int(width * 0.03)))  # transforming image
        image_width = image_Q.get_width()  # getting width of image
        screen.blit(image_Q, (
            (((
                      7.5 * width / 20) + textAcc_width * 1.1 + text_skill_01_width + text_skill_02_width / 2) - image_width / 2),
            lowest_value + 7 * spaceBetween + 4 * text_height + text_skill_02_height * 1.5))
        #   new lowest value
        lowest_value = lowest_value + 10 * spaceBetween + 7 * text_height + 4 * spaceBetween

        # ship number 3

        if vlod5T_mask.overlap(mouse_mask, (mouse_pos[0] - ((5 * width / 20) + vlod5T_rect.x - vlod5T_rect.width / 2),
                                            mouse_pos[1] - (
                                                    lowest_value + 7 * spaceBetween + 4.5 * text_height + vlod5T_rect.y - vlod5T_rect.height / 2))):
            over_vlod5T = True
        else:
            over_vlod5T = False

        # write image
        if over_vlod5T:
            screen.blit(enlarged_vlod5T, ((5 * width / 20) + enlarged_vlod5T_rect.x - vlod5T_rect.width / 2,
                                          lowest_value + 7 * spaceBetween + 4.5 * text_height + vlod5T_rect.y - enlarged_vlod5T_rect.height / 2))
        else:
            screen.blit(vlod5T, ((5 * width / 20) + vlod5T_rect.x - vlod5T_rect.width / 2,
                                 lowest_value + 7 * spaceBetween + 4.5 * text_height + vlod5T_rect.y - vlod5T_rect.height / 2))

        # load info about ship from json
        with open("playerships/playerparams.json", "r") as param_file:
            enemy_param = json.load(param_file)
        Ship_param = enemy_param[2]

        # write info about ship
        if over_vlod5T:
            text = font_name.render("TANK", True, name_color)
            screen.blit(text, ((5 * width / 20) - text.get_width() / 2, lowest_value + 2 * spaceBetween))
            screen.blit(font_text.render(f"{game_text[14]}{Ship_param['hp']}", True, text_color),
                        (7.5 * width / 20, lowest_value + 4 * spaceBetween + text_height))
            screen.blit(font_text.render(f"{game_text[15]}{Ship_param['proj_dmg']}", True, text_color),
                        (7.5 * width / 20, lowest_value + 5 * spaceBetween + 2 * text_height))
            screen.blit(font_text.render(f"{game_text[16]}{Ship_param['fire_rate']}", True, text_color),
                        (7.5 * width / 20, lowest_value + 6 * spaceBetween + 3 * text_height))
            textAcc = font_text.render(f"{game_text[17]}{Ship_param['acceleration']}", True, text_color)
            textAcc_width = textAcc.get_width()  # getting width of text
            screen.blit(textAcc, (7.5 * width / 20, lowest_value + 7 * spaceBetween + 4 * text_height))
            screen.blit(font_text.render(f"{game_text[18]}{Ship_param['max_velocity']}", True, text_color),
                        (7.5 * width / 20, lowest_value + 8 * spaceBetween + 5 * text_height))
        else:
            text = font_name.render("TANK", True, name_color)
            screen.blit(text, ((5 * width / 20) - text.get_width() / 2, lowest_value + 2 * spaceBetween))
            screen.blit(font_text.render(f"{game_text[14]}{Ship_param['hp'][0]}", True, text_color),
                        (7.5 * width / 20, lowest_value + 4 * spaceBetween + text_height))
            screen.blit(font_text.render(f"{game_text[15]}{Ship_param['proj_dmg'][0]}", True, text_color),
                        (7.5 * width / 20, lowest_value + 5 * spaceBetween + 2 * text_height))
            screen.blit(font_text.render(f"{game_text[16]}{Ship_param['fire_rate'][0]}", True, text_color),
                        (7.5 * width / 20, lowest_value + 6 * spaceBetween + 3 * text_height))
            textAcc = font_text.render(f"{game_text[17]}{Ship_param['acceleration'][0]}", True, text_color)
            textAcc_width = textAcc.get_width() + 100  # getting width of text
            screen.blit(textAcc, (7.5 * width / 20, lowest_value + 7 * spaceBetween + 4 * text_height))
            screen.blit(font_text.render(f"{game_text[18]}{Ship_param['max_velocity']}", True, text_color),
                        (7.5 * width / 20, lowest_value + 8 * spaceBetween + 5 * text_height))
        #   skills
        # skill Q
        text_skill_01 = font_text.render(game_text[19], True, text_color)
        text_skill_01_width = text_skill_01.get_width()  # getting width of text
        screen.blit(text_skill_01,
                    (((7.5 * width / 20) + textAcc_width * 1.1), lowest_value + 4 * spaceBetween + text_height))
        text_skill_02 = font_text.render(game_text[25], True, text_color)
        text_skill_02_width = text_skill_02.get_width()  # getting width of text
        text_skill_02_height = text_skill_02.get_height()  # getting height of text
        screen.blit(text_skill_02, (((7.5 * width / 20) + textAcc_width * 1.1 + text_skill_01_width),
                                    lowest_value + 4 * spaceBetween + text_height))
        image_Q = pygame.image.load(
            "assets/images/skills_aboutGame/Q_speedboos_aboutGame.png").convert_alpha()  # load image
        image_Q = pygame.transform.scale(image_Q, (int(width * 0.03), int(width * 0.03)))  # transforming image
        image_width = image_Q.get_width()  # getting width of image
        screen.blit(image_Q, (
            (((
                      7.5 * width / 20) + textAcc_width * 1.1 + text_skill_01_width + text_skill_02_width / 2) - image_width / 2),
            lowest_value + 4 * spaceBetween + text_height + text_skill_02_height * 1.5))
        # skill E
        text_skill_01 = font_text.render(game_text[20], True, text_color)
        text_skill_01_width = text_skill_01.get_width()  # getting width of text
        screen.blit(text_skill_01,
                    (((7.5 * width / 20) + textAcc_width * 1.1), lowest_value + 7 * spaceBetween + 4 * text_height))
        text_skill_02 = font_text.render(game_text[26], True, text_color)
        text_skill_02_width = text_skill_02.get_width()  # getting width of text
        text_skill_02_height = text_skill_02.get_height()  # getting height of text
        screen.blit(text_skill_02, (((7.5 * width / 20) + textAcc_width * 1.1 + text_skill_01_width),
                                    lowest_value + 7 * spaceBetween + 4 * text_height))
        image_Q = pygame.image.load(
            "assets/images/skills_aboutGame/E_gravitypulse_aboutGame.png").convert_alpha()  # load image
        image_Q = pygame.transform.scale(image_Q, (int(width * 0.03), int(width * 0.03)))  # transforming image
        image_width = image_Q.get_width()  # getting width of image
        screen.blit(image_Q, (
            (((
                      7.5 * width / 20) + textAcc_width * 1.1 + text_skill_01_width + text_skill_02_width / 2) - image_width / 2),
            lowest_value + 7 * spaceBetween + 4 * text_height + text_skill_02_height * 1.5))
        #   new lowest value
        lowest_value = lowest_value + 10 * spaceBetween + 7 * text_height + 4 * spaceBetween
        #   enemies
        screen.blit(font_subtitle.render(game_text[27], True, (230, 230, 230)),
                    (3.6 * width / 20, lowest_value + spaceBetween * 4))
        lowest_value = lowest_value + spaceBetween * 4 + subtitle_height
        # enemy number 1
        # load info about ship from json
        with open("enemies/enemyparams.json", "r") as param_file:
            enemy_param = json.load(param_file)
        Ship_param = enemy_param[0]
        # write info about ship
        text = font_name.render("ZAROVKA", True, name_color)
        screen.blit(text, ((5 * width / 20) - text.get_width() / 2, lowest_value + 2 * spaceBetween))
        screen.blit(font_text.render(f"{game_text[14]}{Ship_param['hp']}", True, text_color),
                    (7.5 * width / 20, lowest_value + 4 * spaceBetween + text_height))
        lowest_value_firstText = lowest_value + 4 * spaceBetween + text_height  # variable for loading text in center
        screen.blit(font_text.render(f"{game_text[16]}{Ship_param['dmg']}", True, text_color),
                    (7.5 * width / 20, lowest_value + 5 * spaceBetween + 2 * text_height))
        screen.blit(font_text.render(f"{game_text[17]}{Ship_param['acceleration']}", True, text_color),
                    (7.5 * width / 20, lowest_value + 6 * spaceBetween + 3 * text_height))
        screen.blit(font_text.render(f"{game_text[18]}{Ship_param['max_velocity']}", True, text_color),
                    (7.5 * width / 20, lowest_value + 7 * spaceBetween + 4 * text_height))

        # writen info by myself
        textRect = pygame.Rect(7.5 * width / 20, lowest_value + 9 * spaceBetween + 5 * text_height, 8 * width / 20,
                               50)  # x-axis, y-axis, size on x-axis, size on y-axis
        lowest_value = drawText.drawText(screen, game_text[28], text_color, textRect, font_text, textAlignLeft, True, None)
        # load and write image
        zarovka = pygame.image.load("assets/images/enemy/zarovka/zarovka.png")  # load image
        zarovka = pygame.transform.scale(zarovka, (int(width * 0.053), int(width * 0.08)))  # transforming image
        screen.blit(zarovka, ((5 * width / 20) - zarovka.get_rect().centerx, (
                lowest_value - lowest_value_firstText) / 2 + lowest_value_firstText - zarovka.get_rect().centery))
        lowest_value += 3 * spaceBetween
        # enemy number 2
        # load info about ship from json
        with open("enemies/enemyparams.json", "r") as param_file:
            enemy_param = json.load(param_file)
        Ship_param = enemy_param[1]
        # write info about ship
        text = font_name.render("TANK", True, name_color)
        screen.blit(text, ((5 * width / 20) - text.get_width() / 2, lowest_value + 2 * spaceBetween))
        screen.blit(font_text.render(f"{game_text[14]}{Ship_param['hp']}", True, text_color),
                    (7.5 * width / 20, lowest_value + 4 * spaceBetween + text_height))
        lowest_value_firstText = lowest_value + 4 * spaceBetween + text_height  # variable for loading text in center
        screen.blit(font_text.render(f"{game_text[15]}{Ship_param['proj_dmg']}", True, text_color),
                    (7.5 * width / 20, lowest_value + 5 * spaceBetween + 2 * text_height))
        screen.blit(font_text.render(f"{game_text[16]}{Ship_param['fire_rate']}", True, text_color),
                    (7.5 * width / 20, lowest_value + 6 * spaceBetween + 3 * text_height))
        screen.blit(font_text.render(f"{game_text[17]}{Ship_param['acceleration']}", True, text_color),
                    (7.5 * width / 20, lowest_value + 7 * spaceBetween + 4 * text_height))
        screen.blit(font_text.render(f"{game_text[18]}{Ship_param['max_velocity']}", True, text_color),
                    (7.5 * width / 20, lowest_value + 8 * spaceBetween + 5 * text_height))
        # writen info by myself
        textRect = pygame.Rect(7.5 * width / 20, lowest_value + 10 * spaceBetween + 6 * text_height, 8 * width / 20,
                               50)  # x-axis, y-axis, size on x-axis, size on y-axis
        lowest_value = drawText.drawText(screen, game_text[29], text_color, textRect, font_text, textAlignLeft, True, None)
        # load and write image
        tank = pygame.image.load("assets/images/enemy/tank/tank.png")  # load image
        tank = pygame.transform.scale(tank, (int(width * 0.13), int(width * 0.12)))  # transforming image
        screen.blit(tank, ((5 * width / 20) - tank.get_rect().centerx, (
                lowest_value - lowest_value_firstText) / 2 + lowest_value_firstText - tank.get_rect().centery))
        lowest_value += 3 * spaceBetween
        # enemy number 3
        # load info about ship from json
        with open("enemies/enemyparams.json", "r") as param_file:
            enemy_param = json.load(param_file)
        Ship_param = enemy_param[2]
        # write info about ship
        text = font_name.render("SNIPER", True, name_color)
        screen.blit(text, ((5 * width / 20) - text.get_width() / 2, lowest_value + 2 * spaceBetween))
        screen.blit(font_text.render(f"{game_text[14]}{Ship_param['hp']}", True, text_color),
                    (7.5 * width / 20, lowest_value + 4 * spaceBetween + text_height))
        lowest_value_firstText = lowest_value + 4 * spaceBetween + text_height  # variable for loading text in center
        screen.blit(font_text.render(f"{game_text[15]}{Ship_param['proj_dmg']}", True, text_color),
                    (7.5 * width / 20, lowest_value + 5 * spaceBetween + 2 * text_height))
        screen.blit(font_text.render(f"{game_text[16]}{Ship_param['fire_rate']}", True, text_color),
                    (7.5 * width / 20, lowest_value + 6 * spaceBetween + 3 * text_height))
        screen.blit(font_text.render(f"{game_text[17]}{Ship_param['acceleration']}", True, text_color),
                    (7.5 * width / 20, lowest_value + 7 * spaceBetween + 4 * text_height))
        screen.blit(font_text.render(f"{game_text[18]}{Ship_param['max_velocity']}", True, text_color),
                    (7.5 * width / 20, lowest_value + 8 * spaceBetween + 5 * text_height))
        # writen info by myself
        textRect = pygame.Rect(7.5 * width / 20, lowest_value + 10 * spaceBetween + 6 * text_height, 8 * width / 20,
                               50)  # x-axis, y-axis, size on x-axis, size on y-axis
        lowest_value = drawText.drawText(screen, game_text[30], text_color, textRect, font_text, textAlignLeft, True, None)
        # load and write image
        sniper = pygame.image.load("assets/images/enemy/sniper/sniper.png")  # load image
        sniper = pygame.transform.scale(sniper, (int(width * 0.06), int(width * 0.08)))  # transforming image
        screen.blit(sniper, ((5 * width / 20) - sniper.get_rect().centerx, (
                lowest_value - lowest_value_firstText) / 2 + lowest_value_firstText - sniper.get_rect().centery))
        lowest_value += 3 * spaceBetween
        # enemy number 4
        # load info about ship from json
        with open("enemies/enemyparams.json", "r") as param_file:
            enemy_param = json.load(param_file)
        Ship_param = enemy_param[3]
        # write info about ship
        text = font_name.render("STEALER", True, name_color)
        screen.blit(text, ((5 * width / 20) - text.get_width() / 2, lowest_value + 2 * spaceBetween))
        screen.blit(font_text.render(f"{game_text[14]}{Ship_param['hp']}", True, text_color),
                    (7.5 * width / 20, lowest_value + 4 * spaceBetween + text_height))
        lowest_value_firstText = lowest_value + 4 * spaceBetween + text_height  # variable for loading text in center
        screen.blit(font_text.render(f"{game_text[16]}{Ship_param['dmg']}", True, text_color),
                    (7.5 * width / 20, lowest_value + 5 * spaceBetween + 2 * text_height))
        screen.blit(font_text.render(f"{game_text[17]}{Ship_param['acceleration']}", True, text_color),
                    (7.5 * width / 20, lowest_value + 6 * spaceBetween + 3 * text_height))
        screen.blit(font_text.render(f"{game_text[18]}{Ship_param['max_velocity']}", True, text_color),
                    (7.5 * width / 20, lowest_value + 7 * spaceBetween + 4 * text_height))
        # writen info by myself
        textRect = pygame.Rect(7.5 * width / 20, lowest_value + 9 * spaceBetween + 5 * text_height, 8 * width / 20,
                               50)  # x-axis, y-axis, size on x-axis, size on y-axis
        lowest_value = drawText.drawText(screen, game_text[31], text_color, textRect, font_text, textAlignLeft, True, None)
        # load and write image
        stealer1 = pygame.image.load("assets/images/enemy/stealer/stealer1.png")  # load image
        stealer1 = pygame.transform.scale(stealer1, (int(width * 0.06), int(width * 0.08)))  # transforming image
        screen.blit(stealer1, ((5 * width / 20) - stealer1.get_rect().width * 1.2, (
                lowest_value - lowest_value_firstText) / 2 + lowest_value_firstText - stealer1.get_rect().centery))
        # load and write image
        stealer2 = pygame.image.load("assets/images/enemy/stealer/stealer2.png")  # load image
        stealer2 = pygame.transform.scale(stealer2, (int(width * 0.06), int(width * 0.08)))  # transforming image
        screen.blit(stealer2, ((5 * width / 20) + stealer1.get_rect().width * 0.2, (
                lowest_value - lowest_value_firstText) / 2 + lowest_value_firstText - stealer2.get_rect().centery))
        lowest_value += 3 * spaceBetween
        #   thank you for playing our game
        screen.blit(font_name.render(game_text[32], True, (230, 230, 230)),
                    (3.6 * width / 20, lowest_value + spaceBetween * 4))
        lowest_value = lowest_value + spaceBetween * 4 + 6 * spaceBetween
        #   scroll bar
        # record of biggest lowest_value
        if record:
            lowest_value_first = lowest_value - height
            record = False
        # page ratio for slide bar
        page_ratio = (int(lowest_value_first - (lowest_value - height)) / (lowest_value_first))
        # bars proportions
        bar_pos = [39 / 40 * width, 7 / 40 * height]
        bar_size = [2 / 400 * width, 25 / 40 * height]
        # draw the bar
        pygame.draw.rect(screen, (100, 100, 100), (bar_pos[0], bar_pos[1], bar_size[0], bar_size[1]))
        pygame.draw.rect(screen, (230, 230, 230), (bar_pos[0], bar_pos[1], bar_size[0], bar_size[1] * page_ratio))
        #   event handling
        for event in pg.event.get():
            if event.type == pygame.MOUSEWHEEL:  # 1 mean up, -1 mean down
                if event.y == 1 and y_scroll < 0:  # scroll up
                    if -y_scroll < (0.06 * height):
                        y_scroll = 0
                    else:
                        y_scroll += 0.06 * height
                elif event.y == -1 and lowest_value - height > 0:  # scroll down
                    if (lowest_value - height) < (0.06 * height):
                        y_scroll = (-lowest_value_first)
                    else:
                        y_scroll -= 0.06 * height
            if event.type == pg.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # to cancel
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:  # to quit game
                quit()
        #   cursor
        update_groups([cursor_group], screen)

        clock.tick(GameSetup.fps)
        pygame.display.flip()
