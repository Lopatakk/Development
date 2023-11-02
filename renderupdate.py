import pygame


def render_background(screen):
    background = pygame.image.load("space.png")
    screen.blit(background, (0, 0))


def update_groups(groups, screen):
    for group in groups:
        group.draw(screen)
        group.update()
