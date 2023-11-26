import button
from renderupdate import *


def pause_menu(screen, clock, score, cursor_group):
    game_paused = True
    width, height = screen.get_size()
    font_title = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.05 * width))
    #   surface
    surface = pygame.Surface(screen.get_size())    # creates a new surface of the same dimensions as screen
    surface = surface.convert_alpha()   # making surface transparent
    #   create button instances
    resume_button = button.Button(3.6 * width / 20, 32 * height / 80, "assets/images/button_01.png", 0.3, 0.05, 0.025,'Resume', screen)
    main_menu_button = button.Button(3.6 * width / 20, 41 * height / 80, "assets/images/button_01.png", 0.3, 0.05, 0.025,'Main menu', screen)
    quit_button = button.Button(3.6 * width / 20, 50 * height / 80, "assets/images/button_01.png", 0.3, 0.05, 0.025,'Quit', screen)

    while game_paused:
        background_copy = screen.copy()
        surface.fill((0, 0, 0, 170))  # fill the whole screen with black transparent color
        screen.blit(surface, (0, 0))
        screen.blit(font_title.render("Pause menu", True, (230, 230, 230)), (3.6 * width / 20, 3.4 * height / 20))
        #   BUTTON
        if resume_button.draw_button_and_text(screen):
            return
        if main_menu_button.draw_button_and_text(screen):
            print('main menu')
        if quit_button.draw_button_and_text(screen):
            quit()
        #   closing pause  menu
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # to continue play
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:  # to quit game
                quit()
            if event.type == pygame.QUIT:
                quit()
        #   score and cursor
        render_score(screen, score, 230, 230, 230)
        update_groups([cursor_group], screen)
        clock.tick(ScreenSetup.fps)
        pygame.display.flip()
        screen.blit(background_copy, (0, 0))
