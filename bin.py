import pygame
from pygame.locals import *
from joystick_control import *

pygame.init()
pygame.joystick.init()

joystick = Joystick()

# Inicializace okna
width, height = 800, 600
screen = pygame.display.set_mode((width, height))


# Počáteční pozice čtverce
x, y = width // 2, height // 2
size = 50

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    joystick.update()

    # Omezení pohybu čtverce uvnitř okna
    x = max(0, min(x, width - size))
    y = max(0, min(y, height - size))

    # Vykreslení obrazce
    screen.fill((0, 0, 0))  # Vyčištění obrazovky
    if joystick.cross_button:
        GameSetup.joysticks[0].rumble(0.1, 1, 100)

    if joystick.square_button:
        GameSetup.joysticks[0].rumble(1, 0.1, 100)

    if joystick.triangle_button:
        GameSetup.joysticks[0].rumble(0, 0.1, 100)

    if joystick.circle_button:
        GameSetup.joysticks[0].rumble(1, 1, 100)

    # Obnovování obrazovky
    pygame.display.flip()

pygame.quit()
