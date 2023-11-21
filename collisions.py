import pygame
from explosion import Explosion


def handle_collisions(attacker_group, target_group, kill_attacker, explosion_group):
    hits = pygame.sprite.groupcollide(attacker_group, target_group, dokilla=kill_attacker, dokillb=False, collided=pygame.sprite.collide_mask)
    score_diff = 0
    for attacker, targets_hit in hits.items():
        for target in targets_hit:
            target.hp -= attacker.dmg  # Odebrání životů podle poškození útočníka
            if not kill_attacker:
                attacker.hp -= target.dmg
                if attacker.hp <= 0:
                    explosion = Explosion(attacker.pos, 1)
                    explosion_group.add(explosion)
                    attacker.kill()
                    attacker.mask = None

            if target.hp <= 0:
                score_diff = target.max_hp
                explosion = Explosion(target.pos, 2)
                explosion_group.add(explosion)
                target.kill()  # Odstranění cílového sprite, pokud má životy menší nebo rovno nule
                target.mask = None

    return score_diff
