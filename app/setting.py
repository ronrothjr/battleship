import pygame
from asset_utils import AssetUtils


class Setting:

    def __init__(self, pg: pygame, name: str, setting: dict):
        self.pg = pg
        self.name: str = name
        self.title: str = setting.get('title')
        size = setting.get('size')
        self.w = size["width"]
        self.h = size["height"]
        self.size = (self.w, self.h)
        self.bg: str = setting.get('background', setting.get('bg'))
        self.screen = None
        self.background = None

    def on_init(self):
        if self.bg:
            self.set_bg()

    def on_exit(self):
        pass

    def set_bg(self, width: int=None, height: int=None):
        if width and height:
            size = AssetUtils.get_size_at_max(self.pg, self.w, self.h, (width, height))
        else:
            size = AssetUtils.get_size_at_max(self.pg, self.w, self.h)
        self.screen = self.pg.display.set_mode(size, self.pg.NOFRAME | self.pg.FULLSCREEN | self.pg.RESIZABLE)
        self.background = AssetUtils.get_surface(self.pg, self.bg)
        self.background = self.pg.transform.scale(self.background, size)
        position = AssetUtils.center(self.pg, size[0], size[1])
        self.screen.blit(self.background, position)
