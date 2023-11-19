import pygame
from screensetup import ScreenSetup

height = ScreenSetup.height  # finds height of screen
width = ScreenSetup.width  # finds width of screen
font = pygame.font.Font('assets/fonts/PublicPixel.ttf', 40)
score = 123

new_cursor = pygame.image.load("assets/images/crosshair.png")
new_cursor_rect = new_cursor.get_rect()



def Pause_menu(screen, clock):
    game_paused = True
    pygame.mouse.set_visible(False)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert_alpha()

    while game_paused:
        background_copy = screen.copy()

        surface.fill((100, 100, 100, 150)) # fill the whole screen with black transparent color
        screen.blit(surface, (0, 0))

        # creating rectangles for options
        pause_menu_menu = pygame.draw.rect(screen, (128, 128, 128), [4*width/20, 3*height/20, 800, 100], 0, 10)
        resume_menu = pygame.draw.rect(screen, (128, 128, 128), [4*width/20, 6*height/20, 500, 80], 0, 10)
        main_menu_menu = pygame.draw.rect(screen, (128, 128, 128), [4*width/20, 8*height/20, 500, 80], 0, 10)
        quit_menu = pygame.draw.rect(screen, (128, 128, 128), [4*width/20, 10*height/20, 500, 80], 0, 10)
        score_menu = pygame.draw.rect(screen, (128, 128, 128), [4*width/20, 12*height/20, 500, 80], 0, 10)

        # creating word for rectangles
        screen.blit(font.render("Pause menu", True, "black"), (4.2*width/20, 3.4*height/20))
        screen.blit(font.render("Resume: press ESC", True, "black"), (4.2*width/20, 6.3*height/20))
        screen.blit(font.render("Main menu (neexistuje)", True, "black"), (4.2*width/20, 8.3*height/20))
        screen.blit(font.render("Quit game: press Q", True, "black"), (4.2*width/20, 10.3*height/20))
        score_text = "Score (neexistuje): " + str(score)
        screen.blit(font.render(score_text, True, "black"), (4.2*width/20, 12.3*height/20))

        # closing pause  menu
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:     # to continue play
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:          # to quit game
                quit()
            if event.type == pygame.QUIT:
                quit()

        new_cursor_rect.center = pygame.mouse.get_pos()
        screen.blit(new_cursor, new_cursor_rect)

        pygame.display.flip()

        screen.blit(background_copy, (0, 0))
