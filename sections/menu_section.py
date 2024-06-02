from init_constants import *
from sections import sand_section_cls


class MenuSection:
    def __init__(self):
        pg.init()
        self.font_size = SIDE_MENU_WIDTH // 10
        self.font = pg.font.Font("fonts/Silkscreen.ttf", self.font_size)
        self.side_menu_surface = pg.Surface((SCREEN_WIDTH - SAND_AREA_WIDTH, SCREEN_HEIGHT))

        self.randomness_input_width = SIDE_MENU_WIDTH // 5
        self.randomness_input = pg.Rect(SIDE_MENU_WIDTH / 4, 100, self.randomness_input_width, self.font_size * 1.2)
        self.active_input_color = (0, 250, 250)
        self.inactive_input_color = (255, 255, 255)
        self.current_randomness_color = self.inactive_input_color

        self.randomness_info_text = "0-999"
        self.clear_text = "clear"
        self.snow_text = "snow"
        self.randomness_text = str(sand_section_cls.sand_randomness)

        self.randomness_surface = self.font.render(self.randomness_text, True, self.current_randomness_color)
        self.randomness_info_surface = self.font.render(self.randomness_info_text, True, self.current_randomness_color)

        self.clear_button = pg.Rect(SIDE_MENU_WIDTH / 4, 200, self.font_size * 4, self.font_size * 2)
        self.clear_text_surface = self.font.render(self.clear_text, True, self.current_randomness_color)

        self.snow_button = pg.Rect(SIDE_MENU_WIDTH / 4, 300, self.font_size * 4, self.font_size * 2)
        self.snow_text_surface = self.font.render(self.snow_text, True, "black")

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
        self.side_menu_surface.fill("black")
        self.draw_randomness()
        self.draw_clear_button()
        self.draw_snow_button()
        screen.blit(self.side_menu_surface, (SAND_AREA_WIDTH, 0))

    def set_randomness(self):
        try:
            if int(self.randomness_text) < 1 or int(self.randomness_text) > 1000:
                sand_section_cls.sand_randomness = 1
            else:
                sand_section_cls.sand_randomness = int(self.randomness_text)
        except ValueError:
            pass

    @staticmethod
    def collidepoint_side_menu(surface: pg.Rect, mouse_pos: tuple[int, int]):
        mouse_x = mouse_pos[0] - SAND_AREA_WIDTH
        mouse_y = mouse_pos[1]

        if surface.collidepoint((mouse_x, mouse_y)):
            return True
        return False

    def check_events(self, event: pg.event.EventType):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.collidepoint_side_menu(self.randomness_input, pg.mouse.get_pos()):
                self.current_randomness_color = self.active_input_color
            else:
                self.current_randomness_color = self.inactive_input_color
            if self.collidepoint_side_menu(self.clear_button, pg.mouse.get_pos()):
                sand_section_cls.current_arr = sand_section_cls.make_array_of(0)
                sand_section_cls.old_arr = sand_section_cls.make_array_of(1)
                sand_section_cls.draw_rects()
            if self.collidepoint_side_menu(self.snow_button, pg.mouse.get_pos()):
                sand_section_cls.not_snow_mode = not sand_section_cls.not_snow_mode
                if sand_section_cls.not_snow_mode:
                    sand_section_cls.sand_color = (252, 221, 118)
                else:
                    sand_section_cls.sand_color = "snow"
        if event.type == pg.KEYDOWN:
            if self.current_randomness_color == self.active_input_color:
                if event.key == pg.K_BACKSPACE:
                    self.randomness_text = self.randomness_text[:-1]
                else:
                    self.randomness_text += event.unicode
        self.set_randomness()


menu_section_cls = MenuSection()
