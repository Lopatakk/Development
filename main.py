import pygame
import sys
import time
from player_ship import PlayerShip
from projectile import Projectile
from screensetup import ScreenSetup

# general setup
pygame.init()
clock = pygame.time.Clock()

# screen setup
screen = ScreenSetup.start_setup()

# text
font = pygame.font.Font('freesansbold.ttf', 32)

while True:     # main loop
    background = pygame.image.load("space.png")
    pygame.mouse.set_visible(True)

    # projectiles
    projectile_group = pygame.sprite.Group()

    # player
    player = PlayerShip()
    player_group = pygame.sprite.Group()
    player_group.add(player)

    # rendering
        # background
    screen.blit(background, (0, 0))
        # projectiles
    projectile_group.draw(screen)
    projectile_group.update()
        # triangle
    player_group.draw(screen)
    player_group.update()
        # start text
    text_render = font.render("NEW GAME", True, (255, 255, 255))
    screen.blit(text_render, (ScreenSetup.width / 2.7, ScreenSetup.height / 4))
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
        if player.hp <= 0:
            break

        # key/mouse pressing
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            player.velocity[1] += -1
        if key[pygame.K_s]:
            player.velocity[1] += +1
        if key[pygame.K_a]:
            player.velocity[0] += -1
        if key[pygame.K_d]:
            player.velocity[0] += +1
        if key[pygame.K_SPACE]:
            player.hp += -20
        mouse = pygame.mouse.get_pressed(num_buttons=3)
        if mouse[0]:
            projectile = Projectile("projectile.png", player)
            projectile_group.add(projectile)

        # rendering
            # background
        screen.blit(background, (0, 0))
            # projectiles
        projectile_group.draw(screen)
        projectile_group.update()
            # player
        player_group.draw(screen)
        player_group.update()
            # screen update
        pygame.display.flip()

        print(player.velocity)

        # FPS
        clock.tick(ScreenSetup.fps)

    # start text
    text_render = font.render("SMRT", True, (255, 255, 255))
    screen.blit(text_render, (ScreenSetup.width / 2, ScreenSetup.height / 2))
    # screen update
    pygame.display.flip()

    # wait
    time.sleep(5)
