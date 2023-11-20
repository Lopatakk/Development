import pygame
import button
from screensetup import ScreenSetup

height = ScreenSetup.height  # finds height of screen
width = ScreenSetup.width  # finds width of screen
font_title = pygame.font.Font('assets/fonts/PublicPixel.ttf', 100)
font_text = pygame.font.Font('assets/fonts/PublicPixel.ttf', 30)
new_cursor = pygame.image.load("assets/images/crosshair.png")


def pause_menu(screen, clock, score):
    game_paused = True
    pygame.mouse.set_visible(False)
    new_cursor_rect = new_cursor.get_rect()

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert_alpha()

    # load button images
    button_01_img = pygame.image.load('assets/images/button_01.png').convert_alpha()

    # create button instances
    resume_button = button.Button(4.2 * width / 20, 6 * height / 20, button_01_img, 1, 0.6)
    main_menu_button = button.Button(4.2 * width / 20, 200, button_01_img, 1, 1)


    while game_paused:
        background_copy = screen.copy()

        surface.fill((0, 0, 0, 150))  # fill the whole screen with black transparent color
        screen.blit(surface, (0, 0))
        screen.blit(font_title.render("Pause menu", True, (230, 230, 230)), (4.2 * width / 20, 3.4 * height / 20))


        if resume_button.draw(screen):
            print('resume')
        screen.blit(font_text.render("Resume", True, (50, 50, 50)), (4.2 * width / 20, 6 * height / 20))
        # if main_menu_button.draw(screen):
        #     print('main_menu')

        # closing pause  menu
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # to continue play
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:  # to quit game
                quit()
            if event.type == pygame.QUIT:
                quit()

        new_cursor_rect.center = pygame.mouse.get_pos()
        screen.blit(new_cursor, new_cursor_rect)

        pygame.display.flip()

        screen.blit(background_copy, (0, 0))
