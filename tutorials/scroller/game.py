import pygame, sys, os
from hitcher import Hitcher
from settings import Settings

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


class Game:

    def __init__(self, pg: pygame, Settings: Settings, Hitcher: Hitcher):
        self.settings: Settings = Settings(pg)
        self.hitcher: Hitcher = Hitcher(self.settings)
        self.framePerSec = self.settings.pg.time.Clock()
        self.PAUSED = False

    def start(self):
        self.hitcher.on_start()
        while True:
            now = self.settings.pg.time.get_ticks()
            for event in self.settings.pg.event.get():
                self.handle_pause(event, now)
                if self.is_quitting(event):
                    self.quit()
                move = self.hitcher.get_move(event)
            if not self.PAUSED:
                if not self.hitcher.on_loop(now, move):
                    self.quit()
            self.settings.pg.display.update()
            self.framePerSec.tick(self.settings.fps)

    def handle_pause(self, event, now):
        if self.PAUSED:
            if self.any_key(event):
                self.unpause(now)
        elif not self.PAUSED:
            y = self.get_y(event)
            if self.is_paused(y, event):
                self.pause(now)
        if self.PAUSED:
            self.settings.display.blit(self.settings.paused, ( int(self.settings.screen_width / 2) - 150, int(self.settings.screen_height / 2) - 80) )

    def is_paused(self, y, event):
        return y < 0.3 or event.type == self.settings.pg.KEYDOWN and event.key == self.settings.pg.K_p

    def is_quitting(self, event):
        return event.type == self.settings.pg.QUIT or event.type == self.settings.pg.KEYDOWN and event.key == self.settings.pg.K_ESCAPE

    def quit(self):
        self.settings.pg.quit()
        sys.exit()

    def any_key(self, event):
        return event.type in [self.settings.pg.KEYDOWN, self.settings.pg.MOUSEBUTTONDOWN, self.settings.pg.MOUSEMOTION]

    def pause(self, now):
        self.PAUSED = True
        self.hitcher.on_pause(now)

    def unpause(self, now):
        self.PAUSED = False
        self.hitcher.on_unpause(now)

    def get_y(self, event):
        y = 1
        if event.type == self.settings.pg.MOUSEBUTTONDOWN or event.type == self.settings.pg.MOUSEMOTION:
            pos = event.pos
            y = pos[1] / self.settings.screen_height
        return y


if __name__ == '__main__':
    Game(pygame, Settings, Hitcher).start()
