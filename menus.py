import pygame

import button
from renderupdate import *
from leaderboard import *
import datetime
import drawText

def aboutgame_menu(screen, clock, cursor_group):
    width, height = screen.get_size()
    #   text
    # variables for text
    spaceBetween = 0.01 * width
    textAlignLeft = 0
    textAlignRight = 1
    textAlignCenter = 2
    textAlignBlock = 3
    # fonts for text
    font_title = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.05 * width))    # loading font
    font_subtitle = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.02 * width))    # loading font
    subtitle_height = font_subtitle.size("Tq")[1]   # height of font
    font_text = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.011 * width))    # loading font
    text_height = font_text.size("Tq")[1]   # height of font
    # variable for text y position
    y_scroll = -400
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
        #   event handling
        for event in pg.event.get():
            if event.type == pygame.MOUSEWHEEL:     # 1 means up, -1 means down
                if event.y == 1 and y_scroll < 0:   # scroll up
                    y_scroll += 0.0375 * width
                elif event.y == -1:# and y_scroll > -1000: # scroll down (to maximum bz chtelo nejak omezit pres screen)
                    y_scroll -= 0.0375 * width
            if event.type == pg.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # to cancel
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:  # to quit game
                quit()

        #   about game text
        # about game
        msg = "The game is a 2D arcade-like shooter. The player controls a spaceship and must defend it against enemy attacks. The goal is to score as many points as possible."
        textRect = pygame.Rect(3.6 * width / 20, (27 * height / 80) + y_scroll, 12 * width / 20, 50)  # x-axis, y-axis, size on x-axis, size on y-axis
        lowest_value = drawText.drawText(screen, msg, (230, 230, 230), textRect, font_text, textAlignLeft, True, None)
        # why was created
        msg = "Was created as a semester project in the KEP/VMZ subject on the Faculty of Electrical Engineering, University of West Bohemia. The subject took place in the winter semester of the 2023/24 academic year."
        textRect = pygame.Rect(3.6 * width / 20, lowest_value + spaceBetween * 2, 12 * width / 20, 50)  # x-axis, y-axis, size on x-axis, size on y-axis
        lowest_value = drawText.drawText(screen, msg, (230, 230, 230), textRect, font_text, textAlignLeft, True, None)
        # development team
        screen.blit(font_subtitle.render("Development team", True, (230, 230, 230)), (3.6 * width / 20, lowest_value + spaceBetween * 4))
        lowest_value = lowest_value + spaceBetween * 4 + subtitle_height
        screen.blit(font_text.render("Jan Sebele", True, (230, 230, 230)), (3.6 * width / 20, lowest_value + spaceBetween * 2))
        screen.blit(font_text.render("Pavel Franek", True, (230, 230, 230)), (8 * width / 20, lowest_value + spaceBetween * 2))
        lowest_value = lowest_value + spaceBetween * 2 + text_height
        screen.blit(font_text.render("Michal Lopata", True, (230, 230, 230)), (3.6 * width / 20, lowest_value + spaceBetween))
        screen.blit(font_text.render("Tomas Fikart", True, (230, 230, 230)), (8 * width / 20, lowest_value + spaceBetween))
        lowest_value = lowest_value + spaceBetween + text_height
        # controls
        screen.blit(font_subtitle.render("Controls", True, (230, 230, 230)), (3.6 * width / 20, lowest_value + spaceBetween * 4))
        lowest_value = lowest_value + spaceBetween * 4 + subtitle_height
        screen.blit(font_text.render("Movement:         W–up, S–down, A–left, D–right", True, (230, 230, 230)), (3.6 * width / 20, lowest_value + spaceBetween * 2))
        screen.blit(font_text.render("Aim:              mouse (crosshair)", True, (230, 230, 230)), (3.6 * width / 20, lowest_value + spaceBetween * 3 + text_height))
        screen.blit(font_text.render("Shooting:         left mouse button", True, (230, 230, 230)), (3.6 * width / 20, lowest_value + spaceBetween * 4 + text_height * 2))
        screen.blit(font_text.render("Special skills:   Q and E", True, (230, 230, 230)), (3.6 * width / 20, lowest_value + spaceBetween * 5 + text_height * 3))
        screen.blit(font_text.render("Pause:            ESC", True, (230, 230, 230)), (3.6 * width / 20, lowest_value + spaceBetween * 6 + text_height * 4))
        lowest_value = lowest_value + spaceBetween * 6 + text_height * 5
        #   ships
        screen.blit(font_subtitle.render("Ships", True, (230, 230, 230)), (3.6 * width / 20, lowest_value + spaceBetween * 4))
        lowest_value = lowest_value + spaceBetween * 4 + subtitle_height

        # ship number 1
        # load and write image
        vlod5L = pygame.image.load("assets/images/vlod5L.png")  # load image
        vlod5L = pygame.transform.scale(vlod5L, (int(vlod5L.get_rect().width * 0.8), int(vlod5L.get_rect().height * 0.8)))  # transforming image
        screen.blit(vlod5L, (3.6 * width / 20, lowest_value + 2 * spaceBetween))
        # load info about ship from json
        with open("playerships/playerparams.json", "r") as param_file:
            player_param = json.load(param_file)
        Ship_param = player_param[0]
        # write info about ship
        screen.blit(font_text.render(f"HP: {Ship_param['hp']}", True, (230, 230, 230)), (7.5 * width / 20, lowest_value + 2 * spaceBetween))
        screen.blit(font_text.render(f"DMG: {Ship_param['proj_dmg']}", True, (230, 230, 230)), (7.5 * width / 20, lowest_value + 3 * spaceBetween + text_height))
        screen.blit(font_text.render(f"Fire rate: {Ship_param['fire_rate']}", True, (230, 230, 230)), (7.5 * width / 20, lowest_value + 4 * spaceBetween + 2 * text_height))
        screen.blit(font_text.render(f"Acceleration: {Ship_param['acceleration']}", True, (230, 230, 230)), (7.5 * width / 20, lowest_value + 5 * spaceBetween + 3 * text_height))
        screen.blit(font_text.render(f"Speed: {Ship_param['max_velocity']}", True, (230, 230, 230)), (7.5 * width / 20, lowest_value + 6 * spaceBetween + 4 * text_height))
        screen.blit(font_text.render("Q skill: " + Ship_param['q_skill'], True, (230, 230, 230)), (7.5 * width / 20, lowest_value + 7 * spaceBetween + 5 * text_height))
        screen.blit(font_text.render("E skill: " + Ship_param['e_skill'], True, (230, 230, 230)), (7.5 * width / 20, lowest_value + 8 * spaceBetween + 6 * text_height))
        lowest_value = lowest_value + vlod5L.get_rect().height + 6 * spaceBetween

        # ship number 2
        # load and write image
        vlod5 = pygame.image.load("assets/images/vlod5.png")  # load image
        vlod5 = pygame.transform.scale(vlod5, (int(vlod5.get_rect().width * 0.8), int(vlod5.get_rect().height * 0.8)))  # transforming image
        screen.blit(vlod5, (3.6 * width / 20, lowest_value + 2 * spaceBetween))
        # load info about ship from json
        with open("playerships/playerparams.json", "r") as param_file:
            player_param = json.load(param_file)
        Ship_param = player_param[1]
        # write info about ship
        screen.blit(font_text.render(f"HP: {Ship_param['hp']}", True, (230, 230, 230)), (7.5 * width / 20, lowest_value + 2 * spaceBetween))
        screen.blit(font_text.render(f"DMG: {Ship_param['proj_dmg']}", True, (230, 230, 230)), (7.5 * width / 20, lowest_value + 3 * spaceBetween + text_height))
        screen.blit(font_text.render(f"Fire rate: {Ship_param['fire_rate']}", True, (230, 230, 230)), (7.5 * width / 20, lowest_value + 4 * spaceBetween + 2 * text_height))
        screen.blit(font_text.render(f"Acceleration: {Ship_param['acceleration']}", True, (230, 230, 230)), (7.5 * width / 20, lowest_value + 5 * spaceBetween + 3 * text_height))
        screen.blit(font_text.render(f"Speed: {Ship_param['max_velocity']}", True, (230, 230, 230)), (7.5 * width / 20, lowest_value + 6 * spaceBetween + 4 * text_height))
        screen.blit(font_text.render("Q skill: " + Ship_param['q_skill'], True, (230, 230, 230)), (7.5 * width / 20, lowest_value + 7 * spaceBetween + 5 * text_height))
        screen.blit(font_text.render("E skill: " + Ship_param['e_skill'], True, (230, 230, 230)), (7.5 * width / 20, lowest_value + 8 * spaceBetween + 6 * text_height))
        lowest_value = lowest_value + vlod5.get_rect().height + 6 * spaceBetween

        # ship number 2
        # load and write image
        vlod5T = pygame.image.load("assets/images/vlod5T.png")  # load image
        vlod5T = pygame.transform.scale(vlod5T, (int(vlod5T.get_rect().width * 0.8), int(vlod5T.get_rect().height * 0.8)))  # transforming image
        screen.blit(vlod5T, (3.6 * width / 20, lowest_value + 2 * spaceBetween))
        # load info about ship from json
        with open("playerships/playerparams.json", "r") as param_file:
            player_param = json.load(param_file)
        Ship_param = player_param[2]
        # write info about ship
        screen.blit(font_text.render(f"HP: {Ship_param['hp']}", True, (230, 230, 230)), (7.5 * width / 20, lowest_value + 2 * spaceBetween))
        screen.blit(font_text.render(f"DMG: {Ship_param['proj_dmg']}", True, (230, 230, 230)), (7.5 * width / 20, lowest_value + 3 * spaceBetween + text_height))
        screen.blit(font_text.render(f"Fire rate: {Ship_param['fire_rate']}", True, (230, 230, 230)), (7.5 * width / 20, lowest_value + 4 * spaceBetween + 2 * text_height))
        screen.blit(font_text.render(f"Acceleration: {Ship_param['acceleration']}", True, (230, 230, 230)), (7.5 * width / 20, lowest_value + 5 * spaceBetween + 3 * text_height))
        screen.blit(font_text.render(f"Speed: {Ship_param['max_velocity']}", True, (230, 230, 230)), (7.5 * width / 20, lowest_value + 6 * spaceBetween + 4 * text_height))
        screen.blit(font_text.render("Q skill: " + Ship_param['q_skill'], True, (230, 230, 230)), (7.5 * width / 20, lowest_value + 7 * spaceBetween + 5 * text_height))
        screen.blit(font_text.render("E skill: " + Ship_param['e_skill'], True, (230, 230, 230)), (7.5 * width / 20, lowest_value + 8 * spaceBetween + 6 * text_height))
        lowest_value = lowest_value + vlod5.get_rect().height + 6 * spaceBetween

        #   enemies
        screen.blit(font_subtitle.render("Enemies lode vyse umistit doprostred, takhle to vypada na picu", True, (230, 230, 230)), (3.6 * width / 20, lowest_value + spaceBetween * 4))
        lowest_value = lowest_value + spaceBetween * 4 + subtitle_height





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
    while True:


        # aboutgame_menu(screen, clock, cursor_group)


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
            print("aboutgame")
            aboutgame_menu(screen, clock, cursor_group)
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