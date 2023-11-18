import pygame

x = 250
y = 1000
height = 30
width = 200

def HealthBar(screen, max_hp, player_hp):
    # calculate health ratio
    ratio = player_hp / max_hp
    pygame.draw.rect(screen, "red", (x, y, width, height))
    pygame.draw.rect(screen, "green", (x, y, width * ratio, height))