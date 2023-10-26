import pygame
import numpy as np
from screen_setup import Screen_setup
from ship import Ship


class Player_ship(Ship):
    def __init__(self, picture_path):
        super().__init__()
