import pygame
from asset_utils import AssetUtils


class Setting:

    def __init__(self, pg: pygame, name: str, setting: dict):
        self.pg = pg
        self.name: str = name
        self.title: str = setting.get('title')
        size = setting.get('size')
        self.size = (size['width'], size['height'])
        self.bg: str = setting.get('background', setting.get('bg'))
        self.screen = None
        self.background = None

    def on_init(self):
        if self.bg:
            self.screen = self.pg.display.set_mode(self.size, self.pg.NOFRAME, self.pg.FULLSCREEN)
            self.background = AssetUtils.get_surface(self.pg, self.bg)
            self.screen.blit(self.background, (0,0))

    def on_exit(self):
        pass
