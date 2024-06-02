import sys
import time

from sections import sand_section_cls, menu_section_cls
from init_constants import *


class Game:
    def __init__(self):
        # pg.init() in menu_section
        pg.display.set_caption('sand')

    @staticmethod
    def terminate():
        pg.quit()
        sys.exit()

    def launch(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.terminate()
                sand_section_cls.check_events(event)
                menu_section_cls.check_events(event)

            start_time = time.time()
            sand_section_cls.check_changes()
            print(sand_section_cls.check_changes.__name__, time.time() - start_time)

            start_time = time.time()
            sand_section_cls.draw_rects()
            print(sand_section_cls.draw_rects.__name__, time.time() - start_time)

            menu_section_cls.side_menu()

            pg.display.update()
            clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.launch()
