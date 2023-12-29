import pygame
from explosion import Explosion
from projectileexplosion import ProjectileExplosion
from pygame.sprite import Group


def handle_collisions(attacker_group: Group, is_attacker_projectile: bool, target_group: Group,
                      is_target_projectile: bool, explosion_group: Group):
    hits = pygame.sprite.groupcollide(attacker_group, target_group, dokilla=False, dokillb=False, collided=pygame.sprite.collide_mask)
    score_diff = 0
    for attacker, targets_hit in hits.items():
        for target in targets_hit:
            # projectile to projectile collision
            if is_attacker_projectile and is_target_projectile:
                if attacker.type == "event_horizon_pulse" or attacker.type == "blast":
                    proj_explosion = ProjectileExplosion(attacker.pos, 1)
                    explosion_group.add(proj_explosion)
                    target.kill()

            # projectile to ship collision
            if is_attacker_projectile and not is_target_projectile:
                # damaging target
                target.hp -= attacker.dmg
                # killing the projectile
                proj_explosion = ProjectileExplosion(attacker.pos, 1)
                explosion_group.add(proj_explosion)
                if attacker.type == "normal":
                    attacker.kill()
                # killing target
                if target.hp <= 0:
                    score_diff += target.max_hp
                    explosion = Explosion(target.pos, target.explosion_size)
                    explosion_group.add(explosion)
                    target.kill()
                    target.mask = None

            # ship to ship collision
            if not is_attacker_projectile and not is_target_projectile:
                # damaging target
                target.hp -= attacker.dmg
                # turn off light shield
                if attacker.type == "player_light" and attacker.is_e_action_on:
                    attacker.e_turn_off()
                    attacker.is_e_action_on = False
                    attacker.last_e_use = attacker.time_alive
                else:
                    # damaging attacker
                    attacker.hp -= target.dmg
                    # killing attacker
                    if attacker.hp <= 0:
                        explosion = Explosion(attacker.pos, attacker.explosion_size)
                        explosion_group.add(explosion)
                        attacker.kill()
                        attacker.mask = None
                # killing target
                if target.hp <= 0:
                    score_diff += target.max_hp
                    explosion = Explosion(target.pos, target.explosion_size)
                    explosion_group.add(explosion)
                    target.kill()  # Odstranění cílového sprite, pokud má životy menší nebo rovno nule
                    target.mask = None

    return score_diff


def handle_item_collisions(item_group: Group, ship_group: Group):
    hits = pygame.sprite.groupcollide(item_group, ship_group, dokilla=False, dokillb=False, collided=pygame.sprite.collide_mask)
    for item, ships_hit in hits.items():
        for ship in ships_hit:
            if ship.type == "stealer" or ship.type.startswith("player"):
                if item.type == "medkit":
                    ship.hp += item.heal
                    if ship.hp > ship.max_hp:
                        ship.hp = ship.max_hp
                    pygame.mixer.find_channel(True).play(item.sound)
                    item.kill()
                    item.mask = None
                if ship.type == "stealer":
                    ship.movement = "to_player"
