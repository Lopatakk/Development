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
        pygame.draw.rect(screen, (255, 0, 0), (x, y, size, size))  # Červený čtverec

    # Obnovování obrazovky
    pygame.display.flip()

pygame.quit()
