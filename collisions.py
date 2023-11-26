import pygame
from explosion import Explosion
from projectile_collision import Projectile_collision
from pygame.sprite import Group


def handle_collisions(attacker_group: Group, target_group: Group, is_projectile: bool, explosion_group: Group):
    hits = pygame.sprite.groupcollide(attacker_group, target_group, dokilla=False, dokillb=False, collided=pygame.sprite.collide_mask)
    score_diff = 0
    for attacker, targets_hit in hits.items():
        for target in targets_hit:
            # Odebrání životů podle poškození útočníka
            target.hp -= attacker.dmg
            # projectile to ship collision
            if is_projectile:
                proj_explosion = Projectile_collision(attacker.pos, 1)
                explosion_group.add(proj_explosion)
                attacker.kill()
                attacker.mask = None
            # ship to ship collision
            else:
                attacker.hp -= target.dmg
                if attacker.hp <= 0:
                    explosion = Explosion(attacker.pos, attacker.explosion_size)
                    explosion_group.add(explosion)
                    attacker.kill()
                    attacker.mask = None

            if target.hp <= 0:
                score_diff = target.max_hp
                explosion = Explosion(target.pos, target.explosion_size)
                explosion_group.add(explosion)
                target.kill()  # Odstranění cílového sprite, pokud má životy menší nebo rovno nule
                target.mask = None

    return score_diff
