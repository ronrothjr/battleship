import pygame, os, random
from settings import Settings
from utils import Utils

# abspath = os.path.abspath(__file__)
# dname = os.path.dirname(abspath)
# os.chdir(dname)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, settings: Settings):
        super().__init__()
        self.settings = settings
        self.image = self.settings.pg.image.load(self.settings.get_path('images', "enemy.png"))
        self.image = self.settings.scale_image(self.image)
        self.rect = self.image.get_rect()
        self.lane = self.get_lane()
        x = self.get_x()
        self.rect.center=(x,-self.image.get_height())
        self.mask = self.settings.pg.mask.from_surface(self.image)
        self.speed = settings.enemy_speeds.pop(random.randrange(0, len(self.settings.enemy_speeds)))

    def get_lane(self):
        lane = random.randint(0, self.settings.lanes * 2)
        while not self.is_lane_empty(lane):
            lane = random.randint(0, self.settings.lanes * 2)
        return lane

    def is_lane_empty(self, lane):
        is_empty = True
        for e in self.settings.enemies:
            if e.lane == lane:
                    return False
        return is_empty

    def get_x(self):
        x = self.settings.margin + self.settings.left_shoulder_width + ( self.lane * int( self.settings.tile_width / 2 ) )
        return x
 
    def move(self):
        speed = self.settings.scale(self.settings.speed)
        self.rect.move_ip(0, int( int(speed * 0.65) + int( ( (speed / 2) * self.speed ) ) ))
        if (self.rect.bottom > self.settings.screen_height + self.image.get_height()):
            self.rect.top = 0
            self.lane = self.get_lane()
            x = self.get_x()
            self.rect.center = (x, 0)
