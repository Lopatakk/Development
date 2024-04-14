import button
from renderupdate import *
from leaderboard import *
import datetime
import drawText
from slider import Slider

def settingsPause_menu(screen, clock, cursor_group, background_copy):
    width, height = screen.get_size()
    #   fonts
    font_title = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.05 * width))    # loading font
    font_subTitle = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.018 * width))    # loading font
    font_height = font_subTitle.get_height()
    #   surface and background
    # surface
    surface = pygame.Surface(screen.get_size())  # creates a new surface of the same dimensions as screen
    surface = surface.convert_alpha()  # making surface transparent
    # background
    surface.fill((0, 0, 0, 170))  # fill the whole screen with black transparent color
    #   create button instances
    back_button = button.Button(16 * width / 20, 70 * height / 80, "assets/images/button_01.png", "assets/images/button_02.png", 0.15, 0.05, 0.025, 'Back', screen, "assets/sounds/button_click.mp3", 0.2)
    #   volume
    min_value = 0
    max_value = 10
    with open("settings.json", "r") as settings_file:
        settings = json.load(settings_file)
    music_volume = settings["music_volume"]
    effects_volume = settings["effects_volume"]
    # percentage
    percentageMusic = ((music_volume - min_value) / (max_value - min_value)) * 100
    percentageEffects = ((effects_volume - min_value) / (max_value - min_value)) * 100
    #   sliders
    sliderMusic = Slider((3.6 * width / 20), (27 * height / 80 + font_height * 2), (width * 0.375), (width * 0.015), 0, 100, percentageMusic)
    sliderEffects = Slider((3.6 * width / 20), (37 * height / 80 + font_height * 2), (width * 0.375), (width * 0.015), 0, 100, percentageEffects)
    while True:
        screen.blit(background_copy, (0, 0))
        screen.blit(surface, (0, 0))
        #   text "Settings"
        screen.blit(font_title.render("Settings", True, (230, 230, 230)), (3.6 * width / 20, 3.4 * height / 20))
        #   changing volume
        screen.blit(font_subTitle.render("Music volume", True, (230, 230, 230)), (3.6 * width / 20, 27 * height / 80))
        screen.blit(font_subTitle.render("Effects volume", True, (230, 230, 230)), (3.6 * width / 20, 37 * height / 80))
        #   BUTTON
        if back_button.draw_button_and_text(screen):
            ScreenSetup.music_volume = new_music_volume
            ScreenSetup.effects_volume = new_effects_volume
            settings["music_volume"] = new_music_volume
            settings["effects_volume"] = new_effects_volume
            with open("settings.json", "w") as settings_file:
                json.dump(settings, settings_file, indent=4)
            return
        #   volume
        # music
        sliderMusic.update()
        sliderMusic.draw(screen)
        new_music_volume = min_value + (sliderMusic.get_value_in_percent() / 100) * (max_value - min_value)
        # effects
        sliderEffects.update()
        sliderEffects.draw(screen)
        new_effects_volume = min_value + (sliderEffects.get_value_in_percent() / 100) * (max_value - min_value)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # to cancel
                ScreenSetup.music_volume = new_music_volume
                ScreenSetup.effects_volume = new_effects_volume
                settings["music_volume"] = new_music_volume
                settings["effects_volume"] = new_effects_volume
                with open("settings.json", "w") as settings_file:
                    json.dump(settings, settings_file, indent=4)
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:  # to quit game
                quit()
        #   cursor
        update_groups([cursor_group], screen)

        clock.tick(ScreenSetup.fps)
        pygame.display.flip()

def settingsMain_menu(screen, clock, cursor_group):
    width, height = screen.get_size()
    #   fonts
    font_title = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.05 * width))    # loading font
    font_subTitle = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.018 * width))    # loading font
    font_height = font_subTitle.get_height()
    #   surface and background
    # surface
    surface = pygame.Surface(screen.get_size())    # creates a new surface of the same dimensions as screen
    surface = surface.convert_alpha()   # making surface transparent
    surface.fill((0, 0, 0, 80))  # fill the whole screen with black transparent color
    # background
    background = pygame.image.load("assets/images/Background.png")
    background = pygame.transform.scale(background, (width, height))
    background = pygame.Surface.convert(background)
    #   create button instances
    back_button = button.Button(16 * width / 20, 70 * height / 80, "assets/images/button_01.png", "assets/images/button_02.png", 0.15, 0.05, 0.025, 'Back', screen, "assets/sounds/button_click.mp3", 0.2)
    #   volume
    min_value = 0
    max_value = 10
    with open("settings.json", "r") as settings_file:
        settings = json.load(settings_file)
    music_volume = settings["music_volume"]
    effects_volume = settings["effects_volume"]
    # percentage
    percentageMusic = ((music_volume - min_value) / (max_value - min_value)) * 100
    percentageEffects = ((effects_volume - min_value) / (max_value - min_value)) * 100
    #   sliders
    sliderMusic = Slider((3.6 * width / 20), (27 * height / 80 + font_height * 2), (width * 0.375), (width * 0.015), 0, 100, percentageMusic)
    sliderEffects = Slider((3.6 * width / 20), (37 * height / 80 + font_height * 2), (width * 0.375), (width * 0.015), 0, 100, percentageEffects)
    while True:
        screen.blit(background, (0, 0))
        screen.blit(surface, (0, 0))
        #   text "Settings"
        screen.blit(font_title.render("Settings", True, (230, 230, 230)), (3.6 * width / 20, 3.4 * height / 20))
        #   changing volume
        screen.blit(font_subTitle.render("Music volume", True, (230, 230, 230)), (3.6 * width / 20, 27 * height / 80))
        screen.blit(font_subTitle.render("Effects volume", True, (230, 230, 230)), (3.6 * width / 20, 37 * height / 80))
        #   BUTTON
        if back_button.draw_button_and_text(screen):
            ScreenSetup.music_volume = new_music_volume
            ScreenSetup.effects_volume = new_effects_volume
            settings["music_volume"] = new_music_volume
            settings["effects_volume"] = new_effects_volume
            with open("settings.json", "w") as settings_file:
                json.dump(settings, settings_file, indent=4)
            return
        #   volume
        # music
        sliderMusic.update()
        sliderMusic.draw(screen)
        new_music_volume = min_value + (sliderMusic.get_value_in_percent() / 100) * (max_value - min_value)
        # effects
        sliderEffects.update()
        sliderEffects.draw(screen)
        new_effects_volume = min_value + (sliderEffects.get_value_in_percent() / 100) * (max_value - min_value)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # to cancel
                ScreenSetup.music_volume = new_music_volume
                ScreenSetup.effects_volume = new_effects_volume
                settings["music_volume"] = new_music_volume
                settings["effects_volume"] = new_effects_volume
                with open("settings.json", "w") as settings_file:
                    json.dump(settings, settings_file, indent=4)
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:  # to quit game
                quit()
        #   cursor
        update_groups([cursor_group], screen)

        clock.tick(ScreenSetup.fps)
        pygame.display.flip()

def save_name_menu(screen, clock, cursor_group, score, ship_number):
    width, height = screen.get_size()
    font_title = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.05 * width))
    font_info = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.01 * width))
    #   surface and background
    # surface
    surface = pygame.Surface(screen.get_size())    # creates a new surface of the same dimensions as screen
    surface = surface.convert_alpha()   # making surface transparent
    surface.fill((0, 0, 0, 230))  # fill the whole screen with black transparent color
    # background
    background = pygame.image.load("assets/images/Background.png")
    background = pygame.transform.scale(background, (width, height))
    background = pygame.Surface.convert(background)
    #   create button instances
    save_button = button.Button(3.6 * width / 20, 50 * height / 80, "assets/images/button_01.png", "assets/images/button_02.png", 0.3, 0.05, 0.025,'Save', screen, "assets/sounds/button_click.mp3", 0.2)
    cancel_button = button.Button(3.6 * width / 20, 59 * height / 80, "assets/images/button_01.png",  "assets/images/button_02.png", 0.3, 0.05, 0.025, 'Cancel', screen,"assets/sounds/button_click.mp3", 0.2)
    #   the current date
    date = f'{datetime.datetime.now().date()}'
    #   name input
    user_name = ''
    font_input = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.025 * width))
    text_box = pygame.Rect(3.6 * width / 20, 28 * height / 80, width/2.5, width/20)
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
        pygame.draw.rect(screen, (230, 230, 230), text_box, int(width/300))
        # input text
        text_surface = font_input.render(user_name, True, (230, 230, 230))
        # box is getting bigger with text (min. width, if is text wider, it is adding more width)
        text_box.w = max(width/2.5, text_surface.get_width() + width/50)
        # text
        text_rect = text_surface.get_rect()
        text_rect.centery = text_box.centery    # to get y center of text to y center of box
        text_rect.x = text_box.x + width/100    # to get left side of text to wanted position
        # draw input text on wanted position
        screen.blit(text_surface, text_rect)
        # info about characters and rules when writing name
        screen.blit(font_info.render("maximum 15 characters", True, (150, 150, 150)), (3.6 * width / 20, text_box.y + text_box.height * 1.3))
        screen.blit(font_info.render("only letters, numbers, dots, dashes", True, (150, 150, 150)), (3.6 * width / 20, text_box.y + text_box.height * 1.7))
        #   cursor
        update_groups([cursor_group], screen)

        clock.tick(ScreenSetup.fps)
        pygame.display.flip()

def leaderboard_menu(screen, clock, cursor_group):
    width, height = screen.get_size()
    font_title = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.05 * width))    # loading font
    font_scores_title = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.018 * width))  # loading font
    font_scores = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.014 * width))  # loading font
    #   surface and background
    # surface
    surface = pygame.Surface(screen.get_size())    # creates a new surface of the same dimensions as screen
    surface = surface.convert_alpha()   # making surface transparent
    surface.fill((0, 0, 0, 80))  # fill the whole screen with black transparent color
    # background
    background = pygame.image.load("assets/images/Background.png")
    background = pygame.transform.scale(background, (width, height))
    background = pygame.Surface.convert(background)
    #   create button instances
    back_button = button.Button(16 * width / 20, 70 * height / 80, "assets/images/button_01.png", "assets/images/button_02.png", 0.15, 0.05, 0.025, 'Back', screen, "assets/sounds/button_click.mp3", 0.2)
    #   load the json file.
    highscores = load()
    while True:
        screen.blit(background, (0, 0))
        screen.blit(surface, (0, 0))
        #   text "Leaderboard"
        screen.blit(font_title.render("Scoreboard", True, (230, 230, 230)), (3.6 * width / 20, 3.4 * height / 20))
        #   BUTTON
        if back_button.draw_button_and_text(screen):
            return True
        #   display the high-scores.
        screen.blit(font_scores_title.render("NAME", True, (230, 230, 230)), (3.6 * width / 20, 27 * height / 80))
        screen.blit(font_scores_title.render("SCORE", True, (230, 230, 230)), (8.5 * width / 20, 27 * height / 80))
        screen.blit(font_scores_title.render("SHIP", True, (230, 230, 230)), (11.15 * width / 20, 27 * height / 80))
        screen.blit(font_scores_title.render("DATE", True, (230, 230, 230)), (13.46 * width / 20, 27 * height / 80))
        y_position = list(range(32, 62, 3))     # the number of numbers here makes the number of names in the scoreboard
        for (hi_name, hi_score, hi_selected_ship, hi_date), y in zip(highscores, y_position):
            screen.blit(font_scores.render(f'{hi_name}', True, (160, 160, 160)), (3.6 * width / 20, y * height / 80))
            screen.blit(font_scores.render(f'{hi_score}', True, (160, 160, 160)), (8.5 * width / 20, y * height / 80))
            screen.blit(font_scores.render(f'{hi_selected_ship}', True, (160, 160, 160)), (11.15 * width / 20, y * height / 80))
            screen.blit(font_scores.render(f'{hi_date}', True, (160, 160, 160)), (13.46 * width / 20, y * height / 80))
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

        clock.tick(ScreenSetup.fps)
        pygame.display.flip()

def main_menu(screen, clock, cursor_group):
    width, height = screen.get_size()
    font_title = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.05 * width))
    font_music = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.01 * width))
    #   surface and background
    # surface
    surface = pygame.Surface(screen.get_size())    # creates a new surface of the same dimensions as screen
    surface = surface.convert_alpha()   # making surface transparent
    surface.fill((0, 0, 0, 80))  # fill the whole screen with black transparent color
    # background
    background = pygame.image.load("assets/images/Background.png")
    background = pygame.transform.scale(background, (width, height))
    background = pygame.Surface.convert(background)
    #   create button instances
    play_button = button.Button(3.6 * width / 20, 32 * height / 80, "assets/images/button_01.png", "assets/images/button_02.png", 0.3, 0.05, 0.025, 'Play', screen, "assets/sounds/button_click.mp3", 0.3)
    scoreboard_button = button.Button(3.6 * width / 20, 41 * height / 80, "assets/images/button_01.png", "assets/images/button_02.png", 0.3, 0.05, 0.025, 'Scoreboard', screen, "assets/sounds/button_click.mp3", 0.2)
    aboutgame_button = button.Button(3.6 * width / 20, 50 * height / 80, "assets/images/button_01.png","assets/images/button_02.png", 0.3, 0.05, 0.025, 'About game', screen,"assets/sounds/button_click.mp3", 0.2)
    quit_button = button.Button(3.6 * width / 20, 59 * height / 80, "assets/images/button_01.png", "assets/images/button_02.png", 0.3, 0.05, 0.025,'Quit', screen, "assets/sounds/button_click.mp3", 0.2)
    settings_button = button.Button(149 * (width / 150), width - (149 * (width / 150)), "assets/images/settings_button1.png", "assets/images/settings_button2.png", 0.025, 0.025, 0.01,'', screen, "assets/sounds/button_click.mp3", 0.2)
    while True:
        screen.blit(background, (0, 0))
        screen.blit(surface, (0, 0))
        #   text "Space shooter"            Pavel: Pozdeji by to místo toho možná chtělo nějakou grafickou náhradu
        screen.blit(font_title.render("Space shooter", True, (230, 230, 230)), (3.6 * width / 20, 3.4 * height / 20))
        #   text "Soundtrack: Karl Casey @ White Bat Audio"
        text = font_music.render("Soundtrack by: Karl Casey @ White Bat Audio", True, (150, 150, 150))
        text_width = text.get_width() # width of text
        screen.blit(text, (width - text_width * 1.02, 19.5 * height / 20))
        #   BUTTON
        if play_button.draw_button_and_text(screen):
            return
        if scoreboard_button.draw_button_and_text(screen):
            leaderboard_menu(screen, clock, cursor_group)
        if aboutgame_button.draw_button_and_text(screen):
            aboutgame_menu(screen, clock, cursor_group)
        if quit_button.draw_button_and_text(screen):
            quit()
        if settings_button.draw_image_topRight(screen):
            settingsMain_menu(screen, clock, cursor_group)
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:  # to quit game
                quit()
            if event.type == pygame.QUIT:
                quit()
        #   cursor
        update_groups([cursor_group], screen)

        clock.tick(ScreenSetup.fps)
        pygame.display.flip()

def pause_menu(screen, clock, score, cursor_group):
    width, height = screen.get_size()
    font_title = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.05 * width))
    #   surface and background
    # surface
    surface = pygame.Surface(screen.get_size())    # creates a new surface of the same dimensions as screen
    surface = surface.convert_alpha()   # making surface transparent
    # background
    background_copy = screen.copy()
    surface.fill((0, 0, 0, 170))  # fill the whole screen with black transparent color
    #   create button instances
    resume_button = button.Button(3.6 * width / 20, 32 * height / 80, "assets/images/button_01.png", "assets/images/button_02.png", 0.3, 0.05, 0.025,'Resume', screen, "assets/sounds/button_click.mp3", 0.2)
    main_menu_button = button.Button(3.6 * width / 20, 41 * height / 80, "assets/images/button_01.png", "assets/images/button_02.png", 0.3, 0.05, 0.025,'Main menu', screen, "assets/sounds/button_click.mp3", 0.2)
    quit_button = button.Button(3.6 * width / 20, 50 * height / 80, "assets/images/button_01.png", "assets/images/button_02.png", 0.3, 0.05, 0.025,'Quit', screen, "assets/sounds/button_click.mp3", 0.2)
    settings_button = button.Button(149 * (width / 150), width - (149 * (width / 150)), "assets/images/settings_button1.png", "assets/images/settings_button2.png", 0.025, 0.025, 0.01,'', screen, "assets/sounds/button_click.mp3", 0.2)
    while True:
        screen.blit(background_copy, (0, 0))
        screen.blit(surface, (0, 0))
        #   text "Main Menu"
        screen.blit(font_title.render("Pause menu", True, (230, 230, 230)), (3.6 * width / 20, 3.4 * height / 20))
        #   BUTTON
        if resume_button.draw_button_and_text(screen):
            return False
        if main_menu_button.draw_button_and_text(screen):
            return True
        if quit_button.draw_button_and_text(screen):
            quit()
        if settings_button.draw_image_topRight(screen):
            settingsPause_menu(screen, clock, cursor_group, background_copy)
        #   closing pause  menu
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # to continue play
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:  # to quit game
                quit()
            if event.type == pygame.QUIT:
                quit()
        #   score and cursor
        render_score(screen, score, 230, 230, 230)
        update_groups([cursor_group], screen)

        clock.tick(ScreenSetup.fps)
        pygame.display.flip()

def ship_menu(screen, clock, cursor_group):
    width, height = screen.get_size()
    #   text
    font_title = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.05 * width))
    text = font_title.render("Ship selection", True, (230, 230, 230))
    text_rect = text.get_rect()
    text_rect.centerx = width / 2
    text_rect.y = 3.4 * height / 20
    #   surface and background
    # surface
    surface = pygame.Surface(screen.get_size())    # creates a new surface of the same dimensions as screen
    surface = surface.convert_alpha()   # making surface transparent
    surface.fill((0, 0, 0, 80))  # fill the whole screen with black transparent color
    # background
    background = pygame.image.load("assets/images/Background.png")
    background = pygame.transform.scale(background, (width, height))
    background = pygame.Surface.convert(background)
    #   create button instances
    Light_button = button.Button(2 * width / 8, 8 * height / 16, "assets/images/vlod5L.png", "assets/images/vlod5L.png", 0.08, 0.1, 0.02, 'Light', screen, "assets/sounds/game_start.mp3", 0.3)
    Mid_button = button.Button(4 * width / 8, 8 * height / 16, "assets/images/vlod5.png", "assets/images/vlod5.png", 0.09, 0.1, 0.02, 'Mid', screen, "assets/sounds/game_start.mp3", 0.2)
    Tank_button = button.Button(6 * width / 8, 8 * height / 16, "assets/images/vlod5T.png", "assets/images/vlod5T.png", 0.08, 0.1, 0.02, 'Tank', screen, "assets/sounds/game_start.mp3", 0.2)
    while True:
        screen.blit(background, (0, 0))
        screen.blit(surface, (0, 0))
        #   text "Ship selection"
        screen.blit(text, text_rect)
        #   text of ships properties
        #   button
        if Light_button.draw_image_in_center(screen):
            return 1
        if Mid_button.draw_image_in_center(screen):
            return 2
        if Tank_button.draw_image_in_center(screen):
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

        clock.tick(ScreenSetup.fps)
        pygame.display.flip()

def death_menu(screen, clock, cursor_group, score, ship_number):
    width, height = screen.get_size()
    font_title = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.05 * width))
    font_score = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.025 * width))
    #   surface and background
    # surface
    surface = pygame.Surface(screen.get_size())    # creates a new surface of the same dimensions as screen
    surface = surface.convert_alpha()   # making surface transparent
    surface.fill((0, 0, 0, 230))  # fill the whole screen with black transparent color
    # background
    background = pygame.image.load("assets/images/Background.png")
    background = pygame.transform.scale(background, (width, height))
    background = pygame.Surface.convert(background)
    #   create button instances
    save_name_button = button.Button(3.6 * width / 20, 32 * height / 80, "assets/images/button_01.png","assets/images/button_02.png", 0.3, 0.05, 0.025, 'Save name', screen,"assets/sounds/button_click.mp3", 0.3)
    restart_button = button.Button(3.6 * width / 20, 41 * height / 80, "assets/images/button_01.png", "assets/images/button_02.png", 0.3, 0.05, 0.025, 'Again', screen, "assets/sounds/button_click.mp3", 0.3)
    main_menu_button = button.Button(3.6 * width / 20, 50 * height / 80, "assets/images/button_01.png", "assets/images/button_02.png", 0.3, 0.05, 0.025,'Main menu', screen, "assets/sounds/button_click.mp3", 0.2)
    quit_button = button.Button(3.6 * width / 20, 59 * height / 80, "assets/images/button_01.png", "assets/images/button_02.png", 0.3, 0.05, 0.025,'Quit', screen, "assets/sounds/button_click.mp3", 0.2)
    #   sound
    sound = pygame.mixer.Sound("assets/sounds/game_over.mp3")  # Load sound file
    sound.set_volume(0.6 * ScreenSetup.effects_volume)
    pygame.mixer.find_channel(False).play(sound)
    #   a variable that makes it possible to make the save name button disappear after saving a name
    save_name_clicked = False
    while True:
        screen.blit(background, (0, 0))
        screen.blit(surface, (0, 0))
        #   text "Game over" and "score"
        screen.blit(font_title.render("Game over", True, (230, 230, 230)), (3.6 * width / 20, 3.4 * height / 20))
        score_text = "Score: " + str(score)
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

        clock.tick(ScreenSetup.fps)
        pygame.display.flip()

def aboutgame_menu(screen, clock, cursor_group):
    width, height = screen.get_size()
    #   variable for scroll
    record = True
    y_scroll = 0
    #   text
    # variables for text
    spaceBetween = 0.009 * width
    textAlignLeft = 0
    textAlignRight = 1
    textAlignCenter = 2
    textAlignBlock = 3
    # fonts for text
    font_title = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.05 * width))    # loading font
    title_color = (230, 230, 230)
    font_subtitle = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.02 * width))    # loading font
    subtitle_height = font_subtitle.size("Tq")[1]   # height of font
    font_text = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.01 * width))    # loading font
    text_height = font_text.size("Tq")[1]   # height of font
    text_color = (180, 180, 180)
    font_name = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.012 * width))    # loading font
    name_color = (200, 200, 200)
    #   surface and background
    # surface
    surface = pygame.Surface(screen.get_size())    # creates a new surface of the same dimensions as screen
    surface = surface.convert_alpha()   # making surface transparent
    surface.fill((0, 0, 0, 80))  # fill the whole screen with black transparent color
    # background
    background = pygame.image.load("assets/images/Background.png")
    background = pygame.transform.scale(background, (width, height))
    background = pygame.Surface.convert(background)
    #   create button instances
    back_button = button.Button(16 * width / 20, 70 * height / 80, "assets/images/button_01.png", "assets/images/button_02.png", 0.15, 0.05, 0.025, 'Back', screen, "assets/sounds/button_click.mp3", 0.2)
    while True:
        screen.blit(background, (0, 0))
        screen.blit(surface, (0, 0))
        #   text "About game"
        screen.blit(font_title.render("About game", True, (230, 230, 230)), (3.6 * width / 20, (3.4 * height / 20) + y_scroll))
        #   BUTTON
        if back_button.draw_button_and_text(screen):
            return True
        #   about game text
        # about game
        msg = "The game is a 2D arcade-like shooter. The player controls a spaceship and must defend it against enemy attacks. The goal is to score as many points as possible."
        textRect = pygame.Rect(3.6 * width / 20, (27 * height / 80) + y_scroll, 12 * width / 20, 50)  # x-axis, y-axis, size on x-axis, size on y-axis
        lowest_value = drawText.drawText(screen, msg, text_color, textRect, font_text, textAlignLeft, True, None)
        # why was created
        msg = "Was created as a semester project in the KEP/VMZ subject on the Faculty of Electrical Engineering, University of West Bohemia. The subject took place in the winter semester of the 2023/24 academic year."
        textRect = pygame.Rect(3.6 * width / 20, lowest_value + spaceBetween * 2, 12 * width / 20, 50)  # x-axis, y-axis, size on x-axis, size on y-axis
        lowest_value = drawText.drawText(screen, msg, text_color, textRect, font_text, textAlignLeft, True, None)
        # development team
        screen.blit(font_subtitle.render("Development team", True, title_color), (3.6 * width / 20, lowest_value + spaceBetween * 4))
        lowest_value = lowest_value + spaceBetween * 4 + subtitle_height
        screen.blit(font_text.render("Jan Sebele", True, text_color), (3.6 * width / 20, lowest_value + spaceBetween * 2))
        screen.blit(font_text.render("Pavel Franek", True, text_color), (8 * width / 20, lowest_value + spaceBetween * 2))
        lowest_value = lowest_value + spaceBetween * 2 + text_height
        screen.blit(font_text.render("Michal Lopata", True, text_color), (3.6 * width / 20, lowest_value + spaceBetween))
        screen.blit(font_text.render("Tomas Fikart", True, text_color), (8 * width / 20, lowest_value + spaceBetween))
        lowest_value = lowest_value + spaceBetween + text_height
        # controls
        screen.blit(font_subtitle.render("Controls", True, title_color), (3.6 * width / 20, lowest_value + spaceBetween * 4))
        lowest_value = lowest_value + spaceBetween * 4 + subtitle_height
        screen.blit(font_text.render("Movement:         W–up, S–down, A–left, D–right", True, text_color), (3.6 * width / 20, lowest_value + spaceBetween * 2))
        screen.blit(font_text.render("Aim:              mouse (crosshair)", True, text_color), (3.6 * width / 20, lowest_value + spaceBetween * 3 + text_height))
        screen.blit(font_text.render("Shooting:         left mouse button", True, text_color), (3.6 * width / 20, lowest_value + spaceBetween * 4 + text_height * 2))
        screen.blit(font_text.render("Special skills:   Q and E", True, text_color), (3.6 * width / 20, lowest_value + spaceBetween * 5 + text_height * 3))
        screen.blit(font_text.render("Pause:            ESC", True, text_color), (3.6 * width / 20, lowest_value + spaceBetween * 6 + text_height * 4))
        lowest_value = lowest_value + spaceBetween * 6 + text_height * 5
        #   ships
        screen.blit(font_subtitle.render("Ships", True, title_color), (3.6 * width / 20, lowest_value + spaceBetween * 4))
        lowest_value = lowest_value + spaceBetween * 4 + subtitle_height


        # ship number 1
        # load and write image
        vlod5L = pygame.image.load("assets/images/vlod5L.png")  # load image
        vlod5L = pygame.transform.scale(vlod5L, (int(width * 0.08), int(width * 0.09)))  # transforming image
        screen.blit(vlod5L, ((5 * width / 20) - vlod5L.get_rect().centerx, lowest_value + 7 * spaceBetween + 4.5 * text_height - vlod5L.get_rect().centery))
        # load info about ship from json
        with open("playerships/playerparams.json", "r") as param_file:
            enemy_param = json.load(param_file)
        Ship_param = enemy_param[0]
        # write info about ship
        text = font_name.render("LIGHT", True, name_color)
        screen.blit(text, ((5 * width / 20) - text.get_width() / 2, lowest_value + 2 * spaceBetween))
        screen.blit(font_text.render(f"HP: {Ship_param['hp']}", True, text_color), (7.5 * width / 20, lowest_value + 4 * spaceBetween + text_height))
        screen.blit(font_text.render(f"DMG: {Ship_param['proj_dmg']}", True, text_color), (7.5 * width / 20, lowest_value + 5 * spaceBetween + 2 * text_height))
        screen.blit(font_text.render(f"Fire rate: {Ship_param['fire_rate']}", True, text_color), (7.5 * width / 20, lowest_value + 6 * spaceBetween + 3 * text_height))

        textAcc = font_text.render(f"Acceleration: {Ship_param['acceleration']}", True, text_color)
        textAcc_width = textAcc.get_width()  # getting width of text
        screen.blit(textAcc, (7.5 * width / 20, lowest_value + 7 * spaceBetween + 4 * text_height))

        screen.blit(font_text.render(f"Speed: {Ship_param['max_velocity']}", True, text_color), (7.5 * width / 20, lowest_value + 8 * spaceBetween + 5 * text_height))

        #   skills
        # skill Q
        text_skill_01 = font_text.render("Q skill: ", True, text_color)
        text_skill_01_width = text_skill_01.get_width()  # getting width of text
        screen.blit(text_skill_01, (((7.5 * width / 20) + textAcc_width * 1.2), lowest_value + 4 * spaceBetween + text_height))
        text_skill_02 = font_text.render(Ship_param['q_skill'], True, text_color)
        text_skill_02_width = text_skill_02.get_width()  # getting width of text
        text_skill_02_height = text_skill_02.get_height()  # getting height of text
        screen.blit(text_skill_02, (((7.5 * width / 20) + textAcc_width * 1.2 + text_skill_01_width), lowest_value + 4 * spaceBetween + text_height))
        image_Q = pygame.image.load("assets/images/skills_aboutGame/Q_dash_aboutGame.png").convert_alpha()  # load image
        image_Q = pygame.transform.scale(image_Q, (int(width * 0.06), int(width * 0.06)))  # transforming image
        image_width = image_Q.get_width()  # getting width of image
        screen.blit(image_Q, ((((7.5 * width / 20) + textAcc_width * 1.2 + text_skill_01_width + text_skill_02_width / 2) - image_width / 2), lowest_value + 4 * spaceBetween + text_height + text_skill_02_height * 1.5))
        # skill E
        text_skill_01 = font_text.render("E skill: ", True, text_color)
        text_skill_01_width = text_skill_01.get_width()  # getting width of text
        screen.blit(text_skill_01, (((7.5 * width / 20) + textAcc_width * 1.2), lowest_value + 7 * spaceBetween + 4 * text_height))
        text_skill_02 = font_text.render(Ship_param['e_skill'], True, text_color)
        text_skill_02_width = text_skill_02.get_width()  # getting width of text
        text_skill_02_height = text_skill_02.get_height()  # getting height of text
        screen.blit(text_skill_02, (((7.5 * width / 20) + textAcc_width * 1.2 + text_skill_01_width), lowest_value + 7 * spaceBetween + 4 * text_height))
        image_Q = pygame.image.load("assets/images/skills_aboutGame/E_shield_aboutGame.png").convert_alpha()  # load image
        image_Q = pygame.transform.scale(image_Q, (int(width * 0.06), int(width * 0.06)))  # transforming image
        image_width = image_Q.get_width()  # getting width of image
        screen.blit(image_Q, ((((7.5 * width / 20) + textAcc_width * 1.2 + text_skill_01_width + text_skill_02_width / 2) - image_width / 2), lowest_value + 7 * spaceBetween + 4 * text_height + text_skill_02_height * 1.5))
        #   new lowest value
        lowest_value = lowest_value + 10 * spaceBetween + 7 * text_height + 4 * spaceBetween


        # ship number 2
        # load and write image
        vlod5 = pygame.image.load("assets/images/vlod5.png")  # load image
        vlod5 = pygame.transform.scale(vlod5, (int(width * 0.11), int(width * 0.12)))  # transforming image
        screen.blit(vlod5, ((5 * width / 20) - vlod5.get_rect().centerx, lowest_value + 7 * spaceBetween + 4.5 * text_height - vlod5.get_rect().centery))        # load info about ship from json
        with open("playerships/playerparams.json", "r") as param_file:
            enemy_param = json.load(param_file)
        Ship_param = enemy_param[1]
        # write info about ship
        text = font_name.render("MID", True, name_color)
        screen.blit(text, ((5 * width / 20) - text.get_width() / 2, lowest_value + 2 * spaceBetween))
        screen.blit(font_text.render(f"HP: {Ship_param['hp']}", True, text_color), (7.5 * width / 20, lowest_value + 4 * spaceBetween + text_height))
        screen.blit(font_text.render(f"DMG: {Ship_param['proj_dmg']}", True, text_color), (7.5 * width / 20, lowest_value + 5 * spaceBetween + 2 * text_height))
        screen.blit(font_text.render(f"Fire rate: {Ship_param['fire_rate']}", True, text_color), (7.5 * width / 20, lowest_value + 6 * spaceBetween + 3 * text_height))
        textAcc = font_text.render(f"Acceleration: {Ship_param['acceleration']}", True, text_color)
        textAcc_width = textAcc.get_width()  # getting width of text
        screen.blit(textAcc, (7.5 * width / 20, lowest_value + 7 * spaceBetween + 4 * text_height))
        screen.blit(font_text.render(f"Speed: {Ship_param['max_velocity']}", True, text_color), (7.5 * width / 20, lowest_value + 8 * spaceBetween + 5 * text_height))

        #   skills
        # skill Q
        text_skill_01 = font_text.render("Q skill: ", True, text_color)
        text_skill_01_width = text_skill_01.get_width()  # getting width of text
        screen.blit(text_skill_01, (((7.5 * width / 20) + textAcc_width * 1.2), lowest_value + 4 * spaceBetween + text_height))
        text_skill_02 = font_text.render(Ship_param['q_skill'], True, text_color)
        text_skill_02_width = text_skill_02.get_width()  # getting width of text
        text_skill_02_height = text_skill_02.get_height()  # getting height of text
        screen.blit(text_skill_02, (((7.5 * width / 20) + textAcc_width * 1.2 + text_skill_01_width), lowest_value + 4 * spaceBetween + text_height))
        image_Q = pygame.image.load("assets/images/skills_aboutGame/Q_rapidfire_aboutGame.png").convert_alpha()  # load image
        image_Q = pygame.transform.scale(image_Q, (int(width * 0.06), int(width * 0.06)))  # transforming image
        image_width = image_Q.get_width()  # getting width of image
        screen.blit(image_Q, ((((7.5 * width / 20) + textAcc_width * 1.2 + text_skill_01_width + text_skill_02_width / 2) - image_width / 2), lowest_value + 4 * spaceBetween + text_height + text_skill_02_height * 1.5))
        # skill E
        text_skill_01 = font_text.render("E skill: ", True, text_color)
        text_skill_01_width = text_skill_01.get_width()  # getting width of text
        screen.blit(text_skill_01, (((7.5 * width / 20) + textAcc_width * 1.2), lowest_value + 7 * spaceBetween + 4 * text_height))
        text_skill_02 = font_text.render(Ship_param['e_skill'], True, text_color)
        text_skill_02_width = text_skill_02.get_width()  # getting width of text
        text_skill_02_height = text_skill_02.get_height()  # getting height of text
        screen.blit(text_skill_02, (((7.5 * width / 20) + textAcc_width * 1.2 + text_skill_01_width), lowest_value + 7 * spaceBetween + 4 * text_height))
        image_Q = pygame.image.load("assets/images/skills_aboutGame/E_blastshoot_aboutGame.png").convert_alpha()  # load image
        image_Q = pygame.transform.scale(image_Q, (int(width * 0.06), int(width * 0.06)))  # transforming image
        image_width = image_Q.get_width()  # getting width of image
        screen.blit(image_Q, ((((7.5 * width / 20) + textAcc_width * 1.2 + text_skill_01_width + text_skill_02_width / 2) - image_width / 2), lowest_value + 7 * spaceBetween + 4 * text_height + text_skill_02_height * 1.5))
        #   new lowest value
        lowest_value = lowest_value + 10 * spaceBetween + 7 * text_height + 4 * spaceBetween


        # ship number 3
        # load and write image
        vlod5T = pygame.image.load("assets/images/vlod5T.png")  # load image
        vlod5T = pygame.transform.scale(vlod5T, (int(width * 0.1), int(width * 0.12)))  # transforming image
        screen.blit(vlod5T, ((5 * width / 20) - vlod5T.get_rect().centerx, lowest_value + 7 * spaceBetween + 4.5 * text_height - vlod5T.get_rect().centery))
        # load info about ship from json
        with open("playerships/playerparams.json", "r") as param_file:
            enemy_param = json.load(param_file)
        Ship_param = enemy_param[2]
        # write info about ship
        text = font_name.render("TANK", True, name_color)
        screen.blit(text, ((5 * width / 20) - text.get_width() / 2, lowest_value + 2 * spaceBetween))
        screen.blit(font_text.render(f"HP: {Ship_param['hp']}", True, text_color), (7.5 * width / 20, lowest_value + 4 * spaceBetween + text_height))
        screen.blit(font_text.render(f"DMG: {Ship_param['proj_dmg']}", True, text_color), (7.5 * width / 20, lowest_value + 5 * spaceBetween + 2 * text_height))
        screen.blit(font_text.render(f"Fire rate: {Ship_param['fire_rate']}", True, text_color), (7.5 * width / 20, lowest_value + 6 * spaceBetween + 3 * text_height))

        textAcc = font_text.render(f"Acceleration: {Ship_param['acceleration']}", True, text_color)
        textAcc_width = textAcc.get_width()  # getting width of text
        screen.blit(textAcc, (7.5 * width / 20, lowest_value + 7 * spaceBetween + 4 * text_height))

        screen.blit(font_text.render(f"Speed: {Ship_param['max_velocity']}", True, text_color), (7.5 * width / 20, lowest_value + 8 * spaceBetween + 5 * text_height))


        #   skills
        # skill Q
        text_skill_01 = font_text.render("Q skill: ", True, text_color)
        text_skill_01_width = text_skill_01.get_width()  # getting width of text
        screen.blit(text_skill_01, (((7.5 * width / 20) + textAcc_width * 1.2), lowest_value + 4 * spaceBetween + text_height))
        text_skill_02 = font_text.render(Ship_param['q_skill'], True, text_color)
        text_skill_02_width = text_skill_02.get_width()  # getting width of text
        text_skill_02_height = text_skill_02.get_height()  # getting height of text
        screen.blit(text_skill_02, (((7.5 * width / 20) + textAcc_width * 1.2 + text_skill_01_width), lowest_value + 4 * spaceBetween + text_height))
        image_Q = pygame.image.load("assets/images/skills_aboutGame/Q_speedboos_aboutGame.png").convert_alpha()  # load image
        image_Q = pygame.transform.scale(image_Q, (int(width * 0.06), int(width * 0.06)))  # transforming image
        image_width = image_Q.get_width()  # getting width of image
        screen.blit(image_Q, ((((7.5 * width / 20) + textAcc_width * 1.2 + text_skill_01_width + text_skill_02_width / 2) - image_width / 2), lowest_value + 4 * spaceBetween + text_height + text_skill_02_height * 1.5))
        # skill E
        text_skill_01 = font_text.render("E skill: ", True, text_color)
        text_skill_01_width = text_skill_01.get_width()  # getting width of text
        screen.blit(text_skill_01, (((7.5 * width / 20) + textAcc_width * 1.2), lowest_value + 7 * spaceBetween + 4 * text_height))
        text_skill_02 = font_text.render(Ship_param['e_skill'], True, text_color)
        text_skill_02_width = text_skill_02.get_width()  # getting width of text
        text_skill_02_height = text_skill_02.get_height()  # getting height of text
        screen.blit(text_skill_02, (((7.5 * width / 20) + textAcc_width * 1.2 + text_skill_01_width), lowest_value + 7 * spaceBetween + 4 * text_height))
        image_Q = pygame.image.load("assets/images/skills_aboutGame/E_gravitypulse_aboutGame.png").convert_alpha()  # load image
        image_Q = pygame.transform.scale(image_Q, (int(width * 0.06), int(width * 0.06)))  # transforming image
        image_width = image_Q.get_width()  # getting width of image
        screen.blit(image_Q, ((((7.5 * width / 20) + textAcc_width * 1.2 + text_skill_01_width + text_skill_02_width / 2) - image_width / 2), lowest_value + 7 * spaceBetween + 4 * text_height + text_skill_02_height * 1.5))
        #   new lowest value
        lowest_value = lowest_value + 10 * spaceBetween + 7 * text_height + 4 * spaceBetween


        #   enemies
        screen.blit(font_subtitle.render("Enemies", True, (230, 230, 230)), (3.6 * width / 20, lowest_value + spaceBetween * 4))
        lowest_value = lowest_value + spaceBetween * 4 + subtitle_height
        # enemy number 1
        # load info about ship from json
        with open("enemies/enemyparams.json", "r") as param_file:
            enemy_param = json.load(param_file)
        Ship_param = enemy_param[0]
        # write info about ship
        text = font_name.render("ZAROVKA", True, name_color)
        screen.blit(text, ((5 * width / 20) - text.get_width() / 2, lowest_value + 2 * spaceBetween))
        screen.blit(font_text.render(f"HP: {Ship_param['hp']}", True, text_color), (7.5 * width / 20, lowest_value + 4 * spaceBetween + text_height))
        lowest_value_firstText = lowest_value + 4 * spaceBetween + text_height  # variable for loading text in center
        screen.blit(font_text.render(f"DMG: {Ship_param['dmg']}", True, text_color), (7.5 * width / 20, lowest_value + 5 * spaceBetween + 2 * text_height))
        screen.blit(font_text.render(f"Acceleration: {Ship_param['acceleration']}", True, text_color), (7.5 * width / 20, lowest_value + 6 * spaceBetween + 3 * text_height))
        screen.blit(font_text.render(f"Speed: {Ship_param['max_velocity']}", True, text_color), (7.5 * width / 20, lowest_value + 7 * spaceBetween + 4 * text_height))
        # writen info by myself
        msg = "He acts like a kamikaze pilot. It doesn't have a cannon to shoot, but it deals a lot of damage on contact with a ship."
        textRect = pygame.Rect(7.5 * width / 20, lowest_value + 9 * spaceBetween + 5 * text_height, 8 * width / 20, 50)  # x-axis, y-axis, size on x-axis, size on y-axis
        lowest_value = drawText.drawText(screen, msg, text_color, textRect, font_text, textAlignLeft, True, None)
        # load and write image
        zarovka = pygame.image.load("assets/images/zarovka.png")  # load image
        zarovka = pygame.transform.scale(zarovka, (int(width * 0.053), int(width * 0.08)))  # transforming image
        screen.blit(zarovka, ((5 * width / 20) - zarovka.get_rect().centerx, (lowest_value - lowest_value_firstText)/2 + lowest_value_firstText - zarovka.get_rect().centery))
        lowest_value += 3 * spaceBetween
        # enemy number 2
        # load info about ship from json
        with open("enemies/enemyparams.json", "r") as param_file:
            enemy_param = json.load(param_file)
        Ship_param = enemy_param[1]
        # write info about ship
        text = font_name.render("TANK", True, name_color)
        screen.blit(text, ((5 * width / 20) - text.get_width() / 2, lowest_value + 2 * spaceBetween))
        screen.blit(font_text.render(f"HP: {Ship_param['hp']}", True, text_color), (7.5 * width / 20, lowest_value + 4 * spaceBetween + text_height))
        lowest_value_firstText = lowest_value + 4 * spaceBetween + text_height  # variable for loading text in center
        screen.blit(font_text.render(f"DMG: {Ship_param['proj_dmg']}", True, text_color), (7.5 * width / 20, lowest_value + 5 * spaceBetween + 2 * text_height))
        screen.blit(font_text.render(f"Fire rate: {Ship_param['fire_rate']}", True, text_color), (7.5 * width / 20, lowest_value + 6 * spaceBetween + 3 * text_height))
        screen.blit(font_text.render(f"Acceleration: {Ship_param['acceleration']}", True, text_color), (7.5 * width / 20, lowest_value + 7 * spaceBetween + 4 * text_height))
        screen.blit(font_text.render(f"Speed: {Ship_param['max_velocity']}", True, text_color), (7.5 * width / 20, lowest_value + 8 * spaceBetween + 5 * text_height))
        # writen info by myself
        msg = "His name describes him correctly. He has a lot of HP, he's big, and he shoots fast, but his shots don't do much damage."
        textRect = pygame.Rect(7.5 * width / 20, lowest_value + 10 * spaceBetween + 6 * text_height, 8 * width / 20, 50)  # x-axis, y-axis, size on x-axis, size on y-axis
        lowest_value = drawText.drawText(screen, msg, text_color, textRect, font_text, textAlignLeft, True, None)
        # load and write image
        tank = pygame.image.load("assets/images/tank.png")  # load image
        tank = pygame.transform.scale(tank, (int(width * 0.13), int(width * 0.12)))  # transforming image
        screen.blit(tank, ((5 * width / 20) - tank.get_rect().centerx, (lowest_value - lowest_value_firstText)/2 + lowest_value_firstText - tank.get_rect().centery))
        lowest_value += 3 * spaceBetween
        # enemy number 3
        # load info about ship from json
        with open("enemies/enemyparams.json", "r") as param_file:
            enemy_param = json.load(param_file)
        Ship_param = enemy_param[2]
        # write info about ship
        text = font_name.render("SNIPER", True, name_color)
        screen.blit(text, ((5 * width / 20) - text.get_width() / 2, lowest_value + 2 * spaceBetween))
        screen.blit(font_text.render(f"HP: {Ship_param['hp']}", True, text_color), (7.5 * width / 20, lowest_value + 4 * spaceBetween + text_height))
        lowest_value_firstText = lowest_value + 4 * spaceBetween + text_height  # variable for loading text in center
        screen.blit(font_text.render(f"DMG: {Ship_param['proj_dmg']}", True, text_color), (7.5 * width / 20, lowest_value + 5 * spaceBetween + 2 * text_height))
        screen.blit(font_text.render(f"Fire rate: {Ship_param['fire_rate']}", True, text_color), (7.5 * width / 20, lowest_value + 6 * spaceBetween + 3 * text_height))
        screen.blit(font_text.render(f"Acceleration: {Ship_param['acceleration']}", True, text_color), (7.5 * width / 20, lowest_value + 7 * spaceBetween + 4 * text_height))
        screen.blit(font_text.render(f"Speed: {Ship_param['max_velocity']}", True, text_color), (7.5 * width / 20, lowest_value + 8 * spaceBetween + 5 * text_height))
        # writen info by myself
        msg = "He tries to keep his distance from the ship, making it hard to hit him. His missiles deal a lot of damage, but he has low HP."
        textRect = pygame.Rect(7.5 * width / 20, lowest_value + 10 * spaceBetween + 6 * text_height, 8 * width / 20, 50)  # x-axis, y-axis, size on x-axis, size on y-axis
        lowest_value = drawText.drawText(screen, msg, text_color, textRect, font_text, textAlignLeft, True, None)
        # load and write image
        sniper = pygame.image.load("assets/images/sniper.png")  # load image
        sniper = pygame.transform.scale(sniper, (int(width * 0.06), int(width * 0.08)))  # transforming image
        screen.blit(sniper, ((5 * width / 20) - sniper.get_rect().centerx, (lowest_value - lowest_value_firstText)/2 + lowest_value_firstText - sniper.get_rect().centery))
        lowest_value += 3 * spaceBetween
        # enemy number 4
        # load info about ship from json
        with open("enemies/enemyparams.json", "r") as param_file:
            enemy_param = json.load(param_file)
        Ship_param = enemy_param[3]
        # write info about ship
        text = font_name.render("STEALER", True, name_color)
        screen.blit(text, ((5 * width / 20) - text.get_width() / 2, lowest_value + 2 * spaceBetween))
        screen.blit(font_text.render(f"HP: {Ship_param['hp']}", True, text_color), (7.5 * width / 20, lowest_value + 4 * spaceBetween + text_height))
        lowest_value_firstText = lowest_value + 4 * spaceBetween + text_height  # variable for loading text in center
        screen.blit(font_text.render(f"DMG: {Ship_param['dmg']}", True, text_color), (7.5 * width / 20, lowest_value + 5 * spaceBetween + 2 * text_height))
        screen.blit(font_text.render(f"Acceleration: {Ship_param['acceleration']}", True, text_color), (7.5 * width / 20, lowest_value + 6 * spaceBetween + 3 * text_height))
        screen.blit(font_text.render(f"Speed: {Ship_param['max_velocity']}", True, text_color), (7.5 * width / 20, lowest_value + 7 * spaceBetween + 4 * text_height))
        # writen info by myself
        msg = "Once in a while a MedKit will appear on the screen, if the MedKit is not picked up within a few seconds a Stealer will appear and try to take the MedKit. If you pick it up in front of him, or if he picks it up, his design will change and he'll act like a Zarovka"
        textRect = pygame.Rect(7.5 * width / 20, lowest_value + 9 * spaceBetween + 5 * text_height, 8 * width / 20, 50)  # x-axis, y-axis, size on x-axis, size on y-axis
        lowest_value = drawText.drawText(screen, msg, text_color, textRect, font_text, textAlignLeft, True, None)
        # load and write image
        stealer1 = pygame.image.load("assets/images/stealer1.png")  # load image
        stealer1 = pygame.transform.scale(stealer1, (int(width * 0.06), int(width * 0.08)))  # transforming image
        screen.blit(stealer1, ((5 * width / 20) - stealer1.get_rect().width * 1.2, (lowest_value - lowest_value_firstText)/2 + lowest_value_firstText - stealer1.get_rect().centery))
        # load and write image
        stealer2 = pygame.image.load("assets/images/stealer2.png")  # load image
        stealer2 = pygame.transform.scale(stealer2, (int(width * 0.06), int(width * 0.08)))  # transforming image
        screen.blit(stealer2, ((5 * width / 20) + stealer1.get_rect().width * 0.2, (lowest_value - lowest_value_firstText)/2 + lowest_value_firstText - stealer2.get_rect().centery))
        lowest_value += 3 * spaceBetween
        #   thank you for playing our game
        screen.blit(font_name.render("Thank you for playing our game <3", True, (230, 230, 230)), (3.6 * width / 20, lowest_value + spaceBetween * 4))
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
            if event.type == pygame.MOUSEWHEEL:     # 1 mean up, -1 mean down
                if event.y == 1 and y_scroll < 0:   # scroll up
                    if -y_scroll < (0.06 * height):
                        y_scroll = 0
                    else:
                        y_scroll += 0.06 * height
                elif event.y == -1 and lowest_value - height > 0 : # scroll down
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

        clock.tick(ScreenSetup.fps)
        pygame.display.flip()