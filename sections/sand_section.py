from random import choice

from init_constants import *


class SandSection:
    def __init__(self):
        self.sand_surface = pg.Surface((SAND_AREA_WIDTH, SAND_AREA_HEIGHT))
        self.sand_randomness = 0
        self.sand_randomness_arr = tuple(r for r in range(-self.sand_randomness, self.sand_randomness + 1))

        self.sand_widthness = 1

        self.old_arr = []
        self.current_arr = self.make_array_of(0)
        self.sand_color = (252, 221, 118)

        self.below_tile = None
        self.right_below_tile, self.left_below_tile = None, None
        self.right_tile, self.left_tile = None, None

        self.not_snow_mode = True

        self.mouse_pos_x, self.mouse_pos_y = None, None
        self.arr_pos_x, self.arr_pos_y = None, None

    @staticmethod
    def make_array_of(number: int):
        new_arr = []
        for _ in range(cols + 1):
            new_arr.append([number] * (rows + 1))
        return new_arr

    def detect_sand(self, i: int, j: int):
        if self.old_arr[i][j] == 1:
            return True
        return False

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

    def get_right_below_tile(self, i: int, j: int):
        return self.old_arr[i + 1][j + 1]

    def get_left_below_tile(self, i: int, j: int):
        return self.old_arr[i - 1][j + 1]

    def get_right_tile(self, i: int, j: int):
        return self.old_arr[i + 1][j]

    def get_left_tile(self, i: int, j: int):
        return self.old_arr[i - 1][j]

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
        if self.right_below_tile == 0 and self.right_tile != 1:
            return True
        return False

    def left_below_tile_is_free(self):
        if self.left_below_tile == 0 and self.left_tile != 1:
            return True
        return False

    def check_changes(self):
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
                        self.right_tile = self.get_right_tile(i, j)
                        self.left_tile = self.get_left_tile(i, j)

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

    def draw_rects(self):
        pg.draw.rect(self.sand_surface, "black", (0, 0, SAND_AREA_WIDTH - 1, SAND_AREA_HEIGHT - one_tile_height * 2))
        for i in range(cols):
            for j in range(rows):
                if self.old_arr[i][j] == self.current_arr[i][j] and self.get_below_tile(i, j) != 1:
                    continue
                rect = pg.Rect(i * one_tile_width, j * one_tile_height, one_tile_width, one_tile_height)
                if self.current_arr[i][j] == 1:
                    pg.draw.rect(self.sand_surface, self.sand_color, rect)
        pg.draw.rect(self.sand_surface, "white", (0, 0, SAND_AREA_WIDTH, SAND_AREA_HEIGHT), width=1)
        screen.blit(self.sand_surface, (0, 0))

    def add_grains_randomly(self, x: int, y: int):
        self.sand_randomness_arr = tuple(r for r in range(-self.sand_randomness, self.sand_randomness + 1))
        if self.sand_randomness != 1:
            for i in range(1, self.sand_randomness):
                x_offset = choice(self.sand_randomness_arr)
                y_offset = choice(self.sand_randomness_arr)
                if abs(x + x_offset) > cols or abs(y + y_offset) > rows or \
                        x + x_offset < 0 or y + y_offset < 0:
                    continue
                else:
                    self.current_arr[x + x_offset][y + y_offset] = 1
        else:
            self.current_arr[x][y] = 1

    def add_grains_wider(self, x: int, y: int):
        if self.sand_widthness != 1:
            sand_widthness_range = [w for w in range(-(self.sand_widthness // 2), self.sand_widthness // 2)]
            for i in sand_widthness_range:
                for j in sand_widthness_range:
                    if abs(x + i) > cols or abs(y + j) > rows or \
                            x + i < 0 or y + j < 0:
                        continue
                    self.current_arr[x + i][y + j] = 1
        else:
            self.current_arr[x][y] = 1

    def add_sand(self):
        self.mouse_pos_x = pg.mouse.get_pos()[0]
        self.mouse_pos_y = pg.mouse.get_pos()[1]
        if not self.beyond_window_by_x() and not self.beyond_window_by_y():
            self.arr_pos_x, self.arr_pos_y = self.mouse_pos_x // one_tile_width, self.mouse_pos_y // one_tile_height
            self.add_grains_wider(self.arr_pos_x, self.arr_pos_y)
            self.add_grains_randomly(self.arr_pos_x, self.arr_pos_y)

    def beyond_window_by_x(self):
        if 0 < self.mouse_pos_x < SAND_AREA_WIDTH:
            return False
        return True

    def beyond_window_by_y(self):
        if 0 < self.mouse_pos_y < SAND_AREA_HEIGHT:
            return False
        return True

    def check_events(self, event: pg.event.EventType):
        if any(pg.mouse.get_pressed()):
            self.add_sand()
        if event.type == pg.MOUSEWHEEL:
            if self.sand_widthness > 0:
                self.sand_widthness += event.y
            else:
                self.sand_widthness = 1


sand_section_cls = SandSection()
