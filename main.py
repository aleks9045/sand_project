import sys
import time

from init_constants import *
from sections import sand_section_cls, menu_section_cls


class Game:
    def __init__(self):
        # pg.init() in menu_section
        pg.display.set_caption('sand')

    @staticmethod
    def terminate():
        pg.quit()
        sys.exit()

    def launch(self):
        time_arr_check, time_arr_draw = [], []
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    with open("data.txt", "w") as data:
                        avg_time_arr_check = str(sum(time_arr_check) / len(time_arr_check))
                        avg_time_arr_draw = str(sum(time_arr_draw) / len(time_arr_draw))
                        max_str = "Max: \n check_time\n" + str(max(time_arr_check)) + "\n draw_time\n" + str(
                            max(time_arr_draw)) + "\n"
                        data.write(max_str)
                        avg_str = "Avg: \n check_time\n" + avg_time_arr_check + "\n draw_time\n" + avg_time_arr_draw
                        data.write(avg_str)
                    self.terminate()
                sand_section_cls.check_events(event)
                menu_section_cls.check_events(event)

            start_time = time.time()
            sand_section_cls.check_changes()

            # print(sand_section_cls.check_changes.__name__, time.time() - start_time)
            time_arr_check.append(time.time() - start_time)

            start_time = time.time()
            sand_section_cls.draw_rects()
            # print(sand_section_cls.draw_rects.__name__, time.time() - start_time)
            time_arr_draw.append(time.time() - start_time)

            menu_section_cls.side_menu()

            pg.display.update()
            clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.launch()
