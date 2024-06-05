import pygame as pg


FPS = 60

SCREEN_WIDTH, SCREEN_HEIGHT = 900, 601
SAND_AREA_WIDTH, SAND_AREA_HEIGHT = 601, 601

SIDE_MENU_WIDTH = SCREEN_WIDTH - SAND_AREA_WIDTH

one_tile_width = 5
one_tile_height = 5

cols = SAND_AREA_WIDTH // one_tile_width
rows = SAND_AREA_HEIGHT // one_tile_height

sand_randomness = 0
sand_widthness = 1

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()

