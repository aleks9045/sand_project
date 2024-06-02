import sys
import time
from random import choice

import pygame as pg

FPS = 60

SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600
SAND_AREA_WIDTH, SAND_AREA_HEIGHT = 600, 600

SIDE_MENU_WIDTH = SCREEN_WIDTH - SAND_AREA_WIDTH

one_tile_width = 4
one_tile_height = 4

cols = SAND_AREA_WIDTH // one_tile_width
rows = SAND_AREA_HEIGHT // one_tile_height


class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption('sand')
        self.font_size = SIDE_MENU_WIDTH // 10
        self.font = pg.font.Font("fonts/Silkscreen.ttf", self.font_size)
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pg.time.Clock()

        self.randomness = 3
        self.randomness_arr = tuple(r for r in range(-self.randomness, self.randomness + 1))

        self.old_arr = []
        self.current_arr = self.make_array_of(0)
        self.sand_color = (252, 221, 118)

        self.below_tile = None
        self.right_below_tile, self.left_below_tile = None, None

        self.not_snow_mode = True

        self.mouse_pos_x, self.mouse_pos_y = None, None
        self.arr_pos_x, self.arr_pos_y = None, None

        self.side_menu_surface = pg.Surface((SCREEN_WIDTH - SAND_AREA_WIDTH, SCREEN_HEIGHT))

        self.randomness_input_width = SIDE_MENU_WIDTH // 5
        self.randomness_input = pg.Rect(SAND_AREA_WIDTH + SIDE_MENU_WIDTH / 4, 100,
                                        self.randomness_input_width, self.font_size * 1.2)
        self.active_input_color = (0, 250, 250)
        self.inactive_input_color = (255, 255, 255)
        self.current_randomness_color = self.inactive_input_color

        self.randomness_text = str(self.randomness)
        self.randomness_surface = self.font.render(self.randomness_text, True, self.current_randomness_color)
        self.randomness_info_text = "0-999"
        self.randomness_info_surface = self.font.render(self.randomness_info_text, True, self.current_randomness_color)

        self.clear_button = pg.Rect(SAND_AREA_WIDTH + SIDE_MENU_WIDTH / 4, 200,
                                    self.font_size * 4, self.font_size * 2)
        self.clear_text = "clear"
        self.clear_text_surface = self.font.render(self.clear_text, True, self.current_randomness_color)

        self.snow_button = pg.Rect(SAND_AREA_WIDTH + SIDE_MENU_WIDTH / 4, 300,
                                   self.font_size * 4, self.font_size * 2)
        self.snow_text = "snow"
        self.snow_text_surface = self.font.render(self.snow_text, True, "black")

    @staticmethod
    def terminate():
        pg.quit()
        sys.exit()

    @staticmethod
    def make_array_of(number: int):
        new_arr = []
        for _ in range(cols + 1):
            new_arr.append([number] * (rows + 1))
        return new_arr

    def draw_rects(self):
        start_time = time.time()
        for i in range(cols):
            for j in range(rows):
                if self.old_arr[i][j] == self.current_arr[i][j]:
                    continue
                rect = pg.Rect(i * one_tile_width, j * one_tile_height, one_tile_width, one_tile_height)
                if self.current_arr[i][j] == 1:
                    pg.draw.rect(self.screen, self.sand_color, rect)
                elif self.current_arr[i][j] == 0:
                    pg.draw.rect(self.screen, "black", rect)
        pg.draw.rect(self.screen, "white", (0, 0, SAND_AREA_WIDTH, SAND_AREA_HEIGHT), width=1)
        print(self.draw_rects.__name__, time.time() - start_time)

    def detect_sand(self, i: int, j: int):
        if self.old_arr[i][j] == 1:
            return True
        return False

    def get_right_below_tile(self, i: int, j: int):
        return self.old_arr[i + 1][j + 1]

    def get_left_below_tile(self, i: int, j: int):
        return self.old_arr[i - 1][j + 1]

    @staticmethod
    def detect_bottom_of_window(j: int):
        if j == rows - 1:
            return True
        return False

    @staticmethod
    def on_right_border(i: int):
        if 0 <= i < cols - 1:
            return False
        return True

    @staticmethod
    def on_left_border(i: int):
        if 0 < i <= cols - 1:
            return False
        return True

    def get_below_tile(self, i, j):
        return self.old_arr[i][j + 1]

    def make_current_tile_sand(self, i: int, j: int):
        self.current_arr[i][j] = 1

    def make_below_tile_sand(self, i: int, j: int):
        self.current_arr[i][j + 1] = 1

    def make_random_below_tile_sand(self, i: int, j: int):
        value = choice((-1, 1))
        self.current_arr[i + value][j + 1] = 1

    def make_right_below_tile_sand(self, i, j):
        self.current_arr[i + 1][j + 1] = 1

    def make_left_below_tile_sand(self, i, j):
        self.current_arr[i - 1][j + 1] = 1

    def below_tile_is_free(self):
        if self.below_tile == 0:
            return True
        return False

    def right_below_tile_is_free(self):
        if self.right_below_tile == 0:
            return True
        return False

    def left_below_tile_is_free(self):
        if self.left_below_tile == 0:
            return True
        return False

    def check_changes(self):
        start_time = time.time()
        self.old_arr = self.current_arr
        self.current_arr = self.make_array_of(0)

        for i in range(cols):
            for j in range(rows):
                if self.detect_sand(i, j):

                    if self.detect_bottom_of_window(j):
                        self.make_current_tile_sand(i, j)

                    self.below_tile = self.get_below_tile(i, j)
                    self.right_below_tile, self.left_below_tile = None, None

                    if not self.on_right_border(i):
                        self.right_below_tile = self.get_right_below_tile(i, j)

                    if not self.on_left_border(i):
                        self.left_below_tile = self.get_left_below_tile(i, j)

                    if self.below_tile_is_free() and self.not_snow_mode:
                        self.make_below_tile_sand(i, j)

                    else:

                        if self.right_below_tile_is_free() and self.left_below_tile_is_free():
                            self.make_random_below_tile_sand(i, j)

                        elif self.right_below_tile_is_free() and (
                                not self.left_below_tile_is_free() or self.left_below_tile is None):
                            self.make_right_below_tile_sand(i, j)

                        elif (not self.right_below_tile_is_free() or self.right_below_tile is None) and \
                                self.left_below_tile_is_free():
                            self.make_left_below_tile_sand(i, j)

                        else:
                            self.make_current_tile_sand(i, j)
        print(self.check_changes.__name__, time.time() - start_time)

    def beyond_window_by_x(self):
        if 0 < self.mouse_pos_x < SAND_AREA_WIDTH:
            return False
        return True

    def beyond_window_by_y(self):
        if 0 < self.mouse_pos_y < SAND_AREA_HEIGHT:
            return False
        return True

    def add_grains_randomly(self, x: int, y: int):
        self.randomness_arr = tuple(r for r in range(-self.randomness, self.randomness + 1))
        if self.randomness != 1:
            for i in range(1, self.randomness):
                x_offset = choice(self.randomness_arr)
                y_offset = choice(self.randomness_arr)
                if abs(x + x_offset) > cols or abs(y + y_offset) > rows or \
                        x + x_offset < 0 or y + y_offset < 0:
                    continue
                else:
                    self.current_arr[x + x_offset][y + y_offset] = 1
        else:
            self.current_arr[x][y] = 1

    def add_sand(self):
        self.mouse_pos_x = pg.mouse.get_pos()[0]
        self.mouse_pos_y = pg.mouse.get_pos()[1]
        if not self.beyond_window_by_x() and not self.beyond_window_by_y():
            self.arr_pos_x, self.arr_pos_y = self.mouse_pos_x // one_tile_width, self.mouse_pos_y // one_tile_height
            self.add_grains_randomly(self.arr_pos_x, self.arr_pos_y)

    def draw_randomness(self):
        pg.draw.rect(self.side_menu_surface, "black", self.randomness_input)
        pg.draw.rect(self.side_menu_surface, self.current_randomness_color, self.randomness_input, width=1)
        self.randomness_surface = self.font.render(self.randomness_text, True, self.current_randomness_color)
        self.randomness_input.w = max(self.randomness_input_width, self.randomness_surface.get_width() + 10)

        self.side_menu_surface.blit(self.randomness_surface, (self.randomness_input.x + self.font_size / 10,
                                                              self.randomness_input.y + self.font_size / 10))
        self.side_menu_surface.blit(self.randomness_info_surface, (self.randomness_input.x,
                                                                   self.randomness_input.y - self.font_size))

    def draw_clear_button(self):
        pg.draw.rect(self.side_menu_surface, "darkgreen", self.clear_button, border_radius=7)
        pg.draw.rect(self.side_menu_surface, "green", self.clear_button, 2, border_radius=7)

        self.side_menu_surface.blit(self.clear_text_surface, (self.clear_button.x + self.font_size / 3,
                                                              self.clear_button.y + self.font_size / 2))

    def draw_snow_button(self):
        pg.draw.rect(self.side_menu_surface, "lightblue", self.snow_button, border_radius=7)
        pg.draw.rect(self.side_menu_surface, "snow", self.snow_button, 2, border_radius=7)

        self.side_menu_surface.blit(self.snow_text_surface, (self.snow_button.x + self.font_size / 2,
                                                             self.snow_button.y + self.font_size / 2))

    def side_menu(self):
        self.draw_randomness()
        self.draw_clear_button()
        self.draw_snow_button()
        self.screen.blit(self.side_menu_surface, (SAND_AREA_WIDTH, 0))

    def set_randomness(self):
        try:
            if int(self.randomness_text) < 1 or int(self.randomness_text) > 1000:
                self.randomness = 1
            else:
                self.randomness = int(self.randomness_text)
        except ValueError:
            pass

    def launch(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.terminate()
                if any(pg.mouse.get_pressed()):
                    self.add_sand()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.randomness_input.collidepoint(pg.mouse.get_pos()):
                        self.current_randomness_color = self.active_input_color
                    else:
                        self.current_randomness_color = self.inactive_input_color
                    if self.clear_button.collidepoint(pg.mouse.get_pos()):
                        self.current_arr = self.make_array_of(0)
                        self.old_arr = self.make_array_of(1)
                        self.draw_rects()
                    if self.snow_button.collidepoint(pg.mouse.get_pos()):
                        self.not_snow_mode = not self.not_snow_mode
                        if self.not_snow_mode:
                            self.sand_color = (252, 221, 118)
                        else:
                            self.sand_color = "snow"
                if event.type == pg.KEYDOWN:
                    if self.current_randomness_color == self.active_input_color:
                        if event.key == pg.K_BACKSPACE:
                            self.randomness_text = self.randomness_text[:-1]
                        else:
                            self.randomness_text += event.unicode

                self.set_randomness()

            self.check_changes()
            self.draw_rects()
            self.side_menu()
            pg.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.launch()
