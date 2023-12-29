import button
from renderupdate import *

def ship_menu(screen, clock, cursor_group):
    width, height = screen.get_size()
    font_title = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.05 * width))
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
    Light_button = button.Button(3.6 * width / 20, 32 * height / 80, "assets/images/button_01.png", "assets/images/vlod5L.png", 0.3, 0.05, 0.025, 'Light', screen, "assets/sounds/game_start.mp3", 0.3)
    Mid_button = button.Button(3.6 * width / 20, 41 * height / 80, "assets/images/button_01.png", "assets/images/vlod5.png", 0.3, 0.05, 0.025, 'Mid', screen, "assets/sounds/game_start.mp3", 0.2)
    Tank_button = button.Button(3.6 * width / 20, 50 * height / 80, "assets/images/button_01.png", "assets/images/vlod5T.png", 0.3, 0.05, 0.025, 'Tank', screen, "assets/sounds/game_start.mp3", 0.2)

    while True:
        screen.blit(background, (0, 0))
        screen.blit(surface, (0, 0))
        #   text "Ship selection"
        screen.blit(font_title.render("Ship selection", True, (230, 230, 230)), (3.6 * width / 20, 3.4 * height / 20))
        #   BUTTON
        if Light_button.draw_button_and_text(screen):
            return 1
        if Mid_button.draw_button_and_text(screen):
            return 2
        if Tank_button.draw_button_and_text(screen):
            return 3
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