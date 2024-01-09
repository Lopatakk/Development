import json
from operator import itemgetter
import pygame

import pygame as pg
from pygame import freetype


# pg.init()
# BG_COLOR = pg.Color('gray12')
# BLUE = pg.Color('dodgerblue')
# FONT = freetype.Font(None, 24)


def save(new_highscores):
    try:
        # Načíst existující highscores ze souboru
        with open('highscores.json', 'r') as file:
            existing_highscores = json.load(file)
    except:
        # Pokud soubor neexistuje, vytvoř prázdný seznam
        existing_highscores = []

    # Přidat nová skóre k existujícím
    existing_highscores.extend(new_highscores)

    # Uložit aktualizovaný seznam zpět do souboru
    with open('highscores.json', 'w') as file:
        json.dump(existing_highscores, file)


def load():
    try:
        with open('highscores.json', 'r') as file:
            highscores = json.load(file)  # Read the json file.
    except:
        return []  # Return an empty list if the file doesn't exist.
    # Sorted by the score.
    return sorted(highscores, key=itemgetter(1), reverse=True)