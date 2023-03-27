# Adam Kennedy
# 16/03/2023
# Advanced Higher Project

import pygame as pg
import os

# dirs
LOCAL_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
SCORE_DIR = os.path.join(LOCAL_DIR_PATH, 'highscore')

# display variables
TILE_SIZE = 28
FIELD_W = 10
FIELD_H = 20
FIELD_OFFSET = pg.math.Vector2(10, 10)
SCORE_OFFSET = pg.math.Vector2(318, 42)
DISPLAY_SIZE = (431, 580)
FPS = 60
FIELD_COLOR = (255, 255, 255)
SCORE_BASE = 10
SCORE_MULT = 2
PLAY_AREA_GRID_COLOR = (255, 255, 255)

# end game high score pos
HIGHSCORE_HEADER = 'TOP 5'
HIGHSCORE_HEADER_OFFSET = pg.math.Vector2(20, 50)

PLAYER_HEADER = 'YOUR SCORE'
PLAYER_SCORE_HEADER_OFFSET = pg.math.Vector2(230, 50)
# game start init
INIT_START_POS = (5, 0)

# text
GAME_FONT = 'hellvetica'
FONT_SIZE = 30
ENDGAME_SIZE = 34
TEXT_COLOR = (244, 252, 17)

# shapes
SHAPES = {
    'T':[(0, 0), (-1, 0), (1, 0), (0, 1)],
    'I':[(0, 0), (-1, 0), (-2, 0), (1, 0)],
    'S':[(0, 0), (-1, 0), (0, -1), (1, -1)],
    'Z':[(0, 0), (1, 0), (0, -1), (-1, -1)],
    'L':[(0, 0), (-1, 0), (-1, 1), (1, 0)],
    'J':[(0, 0), (-1, 0), (1, 0), (-1, -1)],
    'O':[(0, 0), (1, 0), (0, -1), (1, -1)]
}

# movement
MOVEMENT_DIR = {
    'left':(-1, 0),
    'right':(1, 0),
    'down':(0, 1)
}

# animation trigger

ANIM_TIME = 240
FAST_ANIM_TIME = 24