import button
from renderupdate import *
import playership

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
    Light_button = button.Button(2 * width / 8, 9 * height / 16, "assets/images/vlod5L.png", "assets/images/vlod5L.png", 0.1, 0.1, 0.02, 'Light', screen, "assets/sounds/game_start.mp3", 0.3)
    Mid_button = button.Button(4 * width / 8, 9 * height / 16, "assets/images/vlod5.png", "assets/images/vlod5.png", 0.1, 0.1, 0.02, 'Mid', screen, "assets/sounds/game_start.mp3", 0.2)
    Tank_button = button.Button(6 * width / 8, 9 * height / 16, "assets/images/vlod5T.png", "assets/images/vlod5T.png", 0.1, 0.1, 0.02, 'Tank', screen, "assets/sounds/game_start.mp3", 0.2)
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
        #   cursor
        update_groups([cursor_group], screen)

        clock.tick(ScreenSetup.fps)
        pygame.display.flip()