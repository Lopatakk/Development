import pygame
import sys
import time
from ship import Ship
from projectile import Projectile
from screen import Screen


# general setup
pygame.init()
clock = pygame.time.Clock()

# screen setup
screen = Screen

# text
font = pygame.font.Font('freesansbold.ttf', 32)

while True:     # main loop
    background = pygame.image.load("space.png")
    pygame.mouse.set_visible(True)

    # projectiles
    projectile_group = pygame.sprite.Group()

    # triangle
    triangle = Ship("vlod.png")
    triangle_group = pygame.sprite.Group()
    triangle_group.add(triangle)

    # rendering
        # background
    screen.blit(background, (0, 0))
        # projectiles
    projectile_group.draw(screen)
    projectile_group.update()
        # triangle
    triangle_group.draw(screen)
    triangle_group.update()
        # start text
    text_render = font.render("NEW GAME", True, (255, 255, 255))
    screen.blit(text_render, (screen.width/2.7, screen.height/4))
        # screen update
    pygame.display.flip()

    # wait
    time.sleep(5)

    while True:     # game loop
        for event in pygame.event.get():
            # closing window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # death
        if triangle.hp <= 0:
            break

        # key/mouse pressing
        key = pygame.key.get_pressed()
        if key[pygame.K_w] == True:
            triangle.velocity[1] += -1
        if key[pygame.K_s] == True:
            triangle.velocity[1] += +1
        if key[pygame.K_a] == True:
            triangle.velocity[0] += -1
        if key[pygame.K_d] == True:
            triangle.velocity[0] += +1
        if key[pygame.K_SPACE] == True:
            triangle.hp += -20
        mouse = pygame.mouse.get_pressed(num_buttons=3)
        if mouse[0]:
            projectile = Projectile("projectile.png", triangle)
            projectile_group.add(projectile)

        # rendering
            # background
        screen.blit(background, (0, 0))
            # projectiles
        projectile_group.draw(screen)
        projectile_group.update()
            # triangle
        triangle_group.draw(screen)
        triangle_group.update()
            # screen update
        pygame.display.flip()

        print(triangle.velocity)

        # FPS
        clock.tick(Screen.fps)

    # start text
    text_render = font.render("SMRT", True, (255, 255, 255))
    screen.blit(text_render, (screen.width/2, screen.height/2))
    # screen update
    pygame.display.flip()

    # wait
    time.sleep(5)