import pygame, os, random
from settings import Settings

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, settings: Settings):
        super().__init__()
        self.settings = settings
        self.image = self.settings.pg.image.load("enemy.png")
        self.rect = self.image.get_rect()
        self.lane = self.get_lane()
        x = settings.MARGIN + settings.LEFT_SHOULDER + ( self.lane * settings.TILE_WIDTH ) - int( settings.TILE_WIDTH / 2 ) - int( self.rect.width / 2 )
        self.rect.center=(x,0)
        self.mask = self.settings.pg.mask.from_surface(self.image)
        self.speed = settings.ENEMY_SPEEDS.pop(random.randrange(0, len(settings.ENEMY_SPEEDS)))

    def get_lane(self):
        lane = random.randint(1, self.settings.LANES * 2)
        while not self.is_lane_empty(lane):
            lane = random.randint(1, self.settings.LANES * 2)
        return lane

    def is_lane_empty(self, lane):
        is_empty = True
        for e in self.settings.enemies:
            if e.lane == lane:
                    return False
        return is_empty
 
    def move(self):
        self.rect.move_ip(0, int( int(self.settings.SPEED * 0.65) + int( ( (self.settings.SPEED / 2) * self.speed ) ) ))
        if (self.rect.bottom > self.settings.SCREEN_HEIGHT + self.image.get_height()):
            self.settings.SCORE += 1
            self.rect.top = 0
            self.lane = self.get_lane()
            x = self.settings.MARGIN + self.settings.LEFT_SHOULDER + ( self.lane * int( self.settings.TILE_WIDTH / 2 ) ) - int( self.settings.TILE_WIDTH / 2 )
            self.rect.center = (x, 0)
