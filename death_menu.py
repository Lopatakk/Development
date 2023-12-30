import button
from renderupdate import *

def death_menu(screen, clock, cursor_group, score):
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
    save_name_button = button.Button(3.6 * width / 20, 32 * height / 80, "assets/images/button_01.png","assets/images/button_01.png", 0.3, 0.05, 0.025, 'Save name', screen,"assets/sounds/button_click.mp3", 0.3)
    restart_button = button.Button(3.6 * width / 20, 41 * height / 80, "assets/images/button_01.png", "assets/images/button_02.png", 0.3, 0.05, 0.025, 'Again', screen, "assets/sounds/button_click.mp3", 0.3)
    main_menu_button = button.Button(3.6 * width / 20, 50 * height / 80, "assets/images/button_01.png", "assets/images/button_02.png", 0.3, 0.05, 0.025,'Main menu', screen, "assets/sounds/button_click.mp3", 0.2)
    quit_button = button.Button(3.6 * width / 20, 59 * height / 80, "assets/images/button_01.png", "assets/images/button_02.png", 0.3, 0.05, 0.025,'Quit', screen, "assets/sounds/button_click.mp3", 0.2)
    #   sound
    sound = pygame.mixer.Sound("assets/sounds/game_over.mp3")  # Load sound file
    sound.set_volume(0.6)
    pygame.mixer.find_channel(True).play(sound)

    while True:
        screen.blit(background, (0, 0))
        screen.blit(surface, (0, 0))
        #   text "Game over" and "score"
        screen.blit(font_title.render("Game over", True, (230, 230, 230)), (3.6 * width / 20, 3.4 * height / 20))
        score_text = "score: " + str(score)
        screen.blit(font_score.render(score_text, True, (230, 230, 230)), (3.6 * width / 20, 5.7 * height / 20))
        #   button
        if save_name_button.draw_button_and_text(screen):
            print("Save name")
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