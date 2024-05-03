import pygame

pygame.init()
screen = pygame.display.set_mode((650, 450))  # Nastavíme velikost okna
pygame.display.set_caption("Transparent Image Example")

# Načtení obrázku
image = pygame.image.load("assets/images/enemy/tank/tank.png").convert_alpha()

# Vytvoření nového obrázku s průhlednými pixely
size = (10, 10)
transparent_image = image.copy()
removed_pixels_image = pygame.Surface(size, pygame.SRCALPHA)
for x in range(size[0]):
    for y in range(size[1]):
        transparent_image.set_at((x+100, y+100), (0, 0, 0, 0))  # Nastavení alfa kanálu na 0 (průhlednost)
        pixel_color = image.get_at((x+100, y+100))  # Získáme barvu pixelu z původního obrázku
        removed_pixels_image.set_at((x, y), pixel_color)

# Smyčka událostí
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Zobrazení nového obrázku s průhlednými pixely
    screen.fill((255, 255, 255))  # Vyplníme obrazovku bílou barvou
    screen.blit(transparent_image, (200, 100))  # Zobrazíme nový obrázek na pozici (0, 0)
    screen.blit(removed_pixels_image, (150, 50))
    pygame.display.flip()  # Aktualizujeme obrazovku

pygame.quit()
