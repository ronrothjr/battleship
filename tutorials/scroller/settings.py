import pygame, os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

class Settings:

    def __init__(self, pg: pygame):
        self.pg: pygame = pg
        pg.init()
        self.BLUE  = (0, 0, 255)
        self.RED   = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        
        self.info = self.pg.display.Info()
        self.SCREEN_WIDTH = self.info.current_w
        self.SCREEN_HEIGHT = self.info.current_h
        self.LEFT_SHOULDER = 41
        self.RIGHT_SHOULDER = 45
        self.LINE_WIDTH = 18
        self.SHOULDER_WIDTH = self.LEFT_SHOULDER + self.RIGHT_SHOULDER
        self.TILE_WIDTH = 134
        self.TILE_HEIGHT = 164
        self.MARGIN = int( ( ( self.SCREEN_WIDTH - self.SHOULDER_WIDTH ) % self.TILE_WIDTH ) / 2 ) + ( self.LINE_WIDTH / 2 )

        self.SPEED = 5
        self.TURN_RADIUS = 30
        self.SCORE = 0
        self.FPS = 60

        self.LANES = int( (self.SCREEN_WIDTH - self.SHOULDER_WIDTH) / self.TILE_WIDTH )
        self.LANES_WIDTH = self.LANES * self.TILE_WIDTH - self.LINE_WIDTH
        self.MAX_ENEMIES = int(self.LANES * 0.6)
        self.SPEED_INC = (0.5) / self.MAX_ENEMIES
        self.ENEMY_SPEEDS = [0.65 + (x * self.SPEED_INC) for x in range(0, self.MAX_ENEMIES)]
        self.MAX_SPEED = 10
        self.DISPLAYSURF = self.pg.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pg.NOFRAME | pg.FULLSCREEN | pg.RESIZABLE)
        self.DISPLAYSURF.fill(self.WHITE)

        self.pg.display.set_caption("Game")
        self.font = self.pg.font.SysFont("Verdana", 60)
        self.font_small = self.pg.font.SysFont("Verdana", 20)
        self.game_over = self.font.render("Game Over", True, self.BLACK)
        self.paused = self.font.render("PAUSED", True, self.BLACK)

        self.tile_image = self.pg.image.load('pavement_tile.png').convert_alpha()
        self.background = self.makeTiledImage( self.tile_image, self.LANES_WIDTH, self.SCREEN_HEIGHT )
        self.left_shoulder = self.pg.image.load('left_shoulder.png').convert_alpha()
        self.right_shoulder = self.pg.image.load('right_shoulder.png').convert_alpha()

        self.enemies = self.pg.sprite.Group()
        self.hitchers = self.pg.sprite.Group()
        self.all_sprites = self.pg.sprite.Group()
        self.SPAWN_ENEMY = 10000
        self.INC_SPEED = 15000
        self.SPAWN_HITCHHIKER = 5000
 
    def makeTiledImage( self, image, width, height ):
        x_cursor = 0
        y_cursor = 0
        tiled_image = self.pg.Surface( ( width, height + (self.TILE_HEIGHT * 2) ) )
        while ( y_cursor < height + image.get_height() ):
            while ( x_cursor < width ):
                tiled_image.blit( image, ( x_cursor, y_cursor ) )
                x_cursor += image.get_width()
            y_cursor += image.get_height()
            x_cursor = 0
        return tiled_image