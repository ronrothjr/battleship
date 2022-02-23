import pygame, os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

class Settings:

    def __init__(self, pg: pygame):
        self.pg: pygame = pg
        pg.init()
        self.blue  = (0, 0, 255)
        self.red   = (255, 0, 0)
        self.green = (0, 255, 0)
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.gray = (128, 128, 128)
        
        self.info = self.pg.display.Info()
        self.screen_width = self.info.current_w
        self.screen_height = self.info.current_h

        self.lanes = 7 # int( (self.screen_width - self.shoulder_width) / self.tile_width )
        self.speed = 5
        self.turn_radius = 30
        self.score = 0
        self.fps = 60

        self.left_shoulder_width = 41
        self.right_shoulder_width = 45
        self.line_width = 18
        self.shoulder_width = self.left_shoulder_width + self.right_shoulder_width
        self.tile_width = 134
        self.tile_height = 164
        self.lanes_width = self.lanes * self.tile_width - self.line_width
        # self.margin = int( ( ( self.screen_width - self.shoulder_width ) % self.tile_width ) / 2 )
        self.margin = int( ( self.screen_width - self.shoulder_width - self.lanes_width ) / 2 )
        self.left_edge = self.margin + self.left_shoulder_width
        self.right_edge = self.screen_width - self.margin - self.right_shoulder_width

        self.max_enemies = int(self.lanes * 0.4)
        self.speed_inc = (0.5) / self.max_enemies
        self.enemy_speeds = [0.65 + (x * self.speed_inc) for x in range(0, self.max_enemies)]
        self.max_speed = 10
        self.display = self.pg.display.set_mode((self.screen_width, self.screen_height), pg.NOFRAME | pg.FULLSCREEN | pg.RESIZABLE)
        self.display.fill(self.white)

        self.pg.display.set_caption("Game")
        self.font = self.pg.font.SysFont("Verdana", 60)
        self.font_small = self.pg.font.SysFont("Verdana", 20)
        self.game_over = self.font.render("Game Over", True, self.black)
        self.paused = self.font.render("PAUSED", True, self.black)

        self.tile_image = self.pg.image.load('pavement_tile.png').convert_alpha()
        self.background = self.makeTiledImage( self.tile_image, self.lanes_width, self.screen_height )
        self.left_shoulder = self.pg.image.load('left_shoulder.png').convert_alpha()
        self.right_shoulder = self.pg.image.load('right_shoulder.png').convert_alpha()

        self.enemies = self.pg.sprite.Group()
        self.hitchers = self.pg.sprite.Group()
        self.all_sprites = self.pg.sprite.Group()
        self.spawn_enemy = 10000
        self.inc_speed = 15000
        self.spawn_hitchhiker = 5000
 
    def makeTiledImage( self, image, width, height ):
        x_cursor = 0
        y_cursor = 0
        tiled_image = self.pg.Surface( ( width, height + (self.tile_height * 2) ) )
        while ( y_cursor < height + image.get_height() ):
            while ( x_cursor < width ):
                tiled_image.blit( image, ( x_cursor, y_cursor ) )
                x_cursor += image.get_width()
            y_cursor += image.get_height()
            x_cursor = 0
        return tiled_image