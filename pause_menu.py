import pygame

def Pause_menu(screen, clock):
    game_paused = True
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert_alpha()

    while game_paused:
        background_copy = screen.copy()

        surface.fill((0, 0, 0, 150))
        screen.blit(surface, (0, 0))

        # closing pause menu
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                return

        pygame.display.flip()

        screen.blit(background_copy, (0, 0))