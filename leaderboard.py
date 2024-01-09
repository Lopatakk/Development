import json
from operator import itemgetter
import pygame as pg

def save(new_highscores):
    try:
        with open('highscores.json', 'r') as file:  # read the json file.
            existing_highscores = json.load(file)
    except:
        existing_highscores = []    # if json is empty, parentheses are loaded into it
    #   add new scores to existing ones
    existing_highscores.extend(new_highscores)
    #   save the updated list back to the file
    with open('highscores.json', 'w') as file:
        json.dump(existing_highscores, file)

def load():
    try:
        with open('highscores.json', 'r') as file:
            highscores = json.load(file)  # read the json file.
    except:
        return []  # return an empty list if the file doesn't exist.
    # sorted by the score.
    return sorted(highscores, key=itemgetter(1), reverse=True)