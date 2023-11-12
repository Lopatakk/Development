import pygame

def handle_collisions(attacker_group, target_group):
    hits = pygame.sprite.groupcollide(attacker_group, target_group, dokilla=True, dokillb=False, collided=pygame.sprite.collide_mask)

    for attacker, targets_hit in hits.items():
        for target in targets_hit:
            target.hp -= attacker.dmg  # Odebrání životů podle poškození útočníka
            if target.hp <= 0:
                target.kill()  # Odstranění cílového sprite, pokud má životy menší nebo rovno nule
                target.mask = None