import pygame
import random
from explosion import Explosion
from projectileexplosion import ProjectileExplosion
from pygame.sprite import Group
from ship_upgrade import ShipUpgrade
from scrap_metal import ScrapMetal
from gamesetup import *


def handle_collisions(joystick, item_group: Group, attacker_group: Group, is_attacker_projectile: bool, target_group: Group,
                      is_target_projectile: bool, explosion_group: Group) -> None | int:
    """
    Handles projectile-to-projectile, projectile-to-ship and ship-to-ship sprite collisions.
    The Following is executed if two sprites collide:

    Projectile-to-projectile: event_horizon_pulse and blast types of projectiles in attacker_group destroys target_group
    projectiles

    Projectile-to-ship: attacker_group projectiles deal damage to target_group ships, if an attacker is of a normal
    type, then it is destroyed, if the target hp is <= 0, then it is destroyed

    Ship-to-ship: attacker_group ships deals damage to target_group ships, if the targets hp is <= 0, then it is
    destroyed, if an attacker is of player_light type and the shield is on, then it gets turned off, else an attacker
    gets damaged and if its hp is <= 0, then it is destroyed
    :param item_group: Group of all items
    :param attacker_group: Group of attacking sprites
    :param is_attacker_projectile: True if attackers are projectiles
    :param target_group: Group of targeted sprites
    :param is_target_projectile: True if targets are projectiles
    :param explosion_group: Sprite group for storing explosions
    :return: if a collision type is ship-to-ship or projectile-to-ship and any targets are destroyed, returns according score, otherwise None
    """
    hits = pygame.sprite.groupcollide(attacker_group, target_group, dokilla=False, dokillb=False, collided=pygame.sprite.collide_mask)
    score_diff = 0
    for attacker, targets_hit in hits.items():
        for target in targets_hit:

            # projectile to projectile collision
            if is_attacker_projectile and is_target_projectile:
                if attacker.type == "event_horizon_pulse" or attacker.type == "blast":
                    proj_explosion = ProjectileExplosion(attacker.pos, 1, target.color)
                    explosion_group.add(proj_explosion)
                    target.kill()

            # projectile to ship collision
            if is_attacker_projectile and not is_target_projectile:
                # vibrations
                if target.type == "player_light" or target.type == "player_mid" or target.type == "player_tank":
                    if joystick.active:
                        if GameSetup.vibrations:
                            GameSetup.joysticks[0].stop_rumble()
                            GameSetup.vibration_start = target.time_alive
                            GameSetup.vibration_time = 200
                            GameSetup.joysticks[0].rumble(1, 1, GameSetup.vibration_time)
                # damaging target
                target.hp -= attacker.dmg
                if target.type == 'tank':
                    spawn_scrap_metal(item_group, target, {1: 0.05})
                else:
                    spawn_scrap_metal(item_group, target, {1: 0.1})
                # killing the projectile
                if attacker.type == "normal" or attacker.type == "blast":
                    proj_explosion = ProjectileExplosion(attacker.pos, 1, attacker.color)
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

                    # spawning items
                    if target.type == 'tank':
                        spawn_ship_upgrade(item_group, target)
                    else:
                        spawn_scrap_metal(item_group, target, {1: 0.3, 2: 0.1, 3: 0.1})

            # ship to ship collision
            if not is_attacker_projectile and not is_target_projectile:
                # vibrations
                if attacker.type == "player_light" or attacker.type == "player_mid" or attacker.type == "player_tank":
                    if joystick.active:
                        if GameSetup.vibrations:
                            GameSetup.joysticks[0].stop_rumble()
                            GameSetup.vibration_start = attacker.time_alive
                            GameSetup.vibration_time = 500
                            GameSetup.joysticks[0].rumble(1, 1, GameSetup.vibration_time)
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

                    # spawning items
                    if target.type == 'tank':
                        spawn_ship_upgrade(item_group, target)
                    else:
                        spawn_scrap_metal(item_group, target, {1: 0.5, 2: 0.2, 3: 0.2})

    return score_diff


def spawn_ship_upgrade(item_group, target):
    modules = {
        "weapons": 0.2,
        "cooling": 0.2,
        "repair_module": 0.2,
        "shield": 0.2,
        "booster": 0.2
    }
    rand_num = random.random()
    cumulative_probability = 0  # acumulating the probability of the last items
    for module, probability in modules.items():
        cumulative_probability += probability  # adding actual probability to acumulated probability
        if rand_num < cumulative_probability:
            ship_upgrade = ShipUpgrade(target.pos, module, True, target.velocity, target.velocity_coefficient)
            item_group.add(ship_upgrade)
            break


def spawn_scrap_metal(item_group, target, probability):
    rand_num = random.random()
    scrap_metal_prob = probability
    cumulative_probability = 0  # acumulating the probability of the last items

    for number, probability in scrap_metal_prob.items():
        cumulative_probability += probability  # adding actual probability to acumulated probability
        if rand_num < cumulative_probability:
            for i in range(number):
                rand_dir_x = random.uniform(0.25, 1.5)
                rand_dir_y = random.uniform(0.25, 1.5)
                scrap_metal = ScrapMetal(target.pos, (target.velocity[0] * rand_dir_x, target.velocity[1] * rand_dir_y),
                                         target.velocity_coefficient)
                item_group.add(scrap_metal)
            break


def handle_item_collisions(item_group: Group, ship_group: Group, storage_items, scrap_metal_count) -> str:
    """
    Handles item-to-ship collisions for medkits and player, stealer types of ships or upgrade parts.
    If any sprite from item_group collides with any sprite from ship_group, then the ships hp increase and the item
    disappears. If the ship is of stealer type, the collision also changes its movement target to the player.
    :param scrap_metal_count: Number of collected scrap metal
    :param storage_items: Collecting items to storage
    :param item_group: Sprite group of a pickable items
    :param ship_group: Sprite group with ships that can pick item
    :return: None
    """
    hits = pygame.sprite.groupcollide(item_group, ship_group, dokilla=False, dokillb=False, collided=pygame.sprite.collide_mask)
    for item, ships_hit in hits.items():
        for ship in ships_hit:
            if ship.type == "stealer" or ship.type.startswith("player"):
                if item.type == "medkit":
                    ship.hp += item.heal
                    if ship.hp > ship.max_hp:
                        ship.hp = ship.max_hp
                    pygame.mixer.find_channel(False).play(item.sound)
                    item.kill()
                    item.mask = None
                    if ship.type == "stealer":
                        ship.movement = "to_player"
                        ship.image_non_rot = ship.image_non_rot_orig_with_medkit
                        ship.took_item = True
                if item.type == "ship_upgrade":
                    if len(storage_items) < 4:
                        storage_items.append(item)
                    pygame.mixer.find_channel(False).play(item.sound)
                    item.kill()
                    item.mask = None
                    return "game_paused_upgrade"
                if item.type == "scrap_metal":
                    pygame.mixer.find_channel(False).play(item.sound)
                    item.kill()
                    item.mask = None
                    return "scrap_metal_collected"

#
# def remove_pixels(image, rect):
#     transparent_image = image.copy()
#     removed_pixels_image = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
#     for x in range(rect.width):
#         for y in range(rect.height):
#             transparent_image.set_at((x + rect.x, y + rect.y), (0, 0, 0, 0))
#             pixel_color = image.get_at((x + rect.x, y + rect.y))
#             removed_pixels_image.set_at((x, y), pixel_color)
#     return transparent_image, removed_pixels_image
