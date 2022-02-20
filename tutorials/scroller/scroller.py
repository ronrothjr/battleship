#pylint:disable=E0602
import pygame, sys, os, random, time
from pygame.locals import *

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
 
pygame.init()
 
FPS = 60
FramePerSec = pygame.time.Clock()
 
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h
LEFT_SHOULDER = 41
RIGHT_SHOULDER = 45
SHOULDER_WIDTH = LEFT_SHOULDER + RIGHT_SHOULDER
TILE_WIDTH = 134
TILE_HEIGHT = 164
OFFSET_WIDTH = int( ( ( SCREEN_WIDTH - SHOULDER_WIDTH ) % TILE_WIDTH ) / 2 )
SPEED = 5
SCORE = 0

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)
background = pygame.image.load("AnimatedStreet.png")
 
def makeTiledImage( image, width, height ):
    x_cursor = 0
    y_cursor = 0

    tiled_image = pygame.Surface( ( width, height + (TILE_HEIGHT * 2) ) )
    while ( y_cursor < height + image.get_height() ):
        while ( x_cursor < width ):
            tiled_image.blit( image, ( x_cursor, y_cursor ) )
            x_cursor += image.get_width()
        y_cursor += image.get_height()
        x_cursor = 0
    return tiled_image
LANES_WIDTH = int( (SCREEN_WIDTH - SHOULDER_WIDTH) / TILE_WIDTH ) * TILE_WIDTH
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME | pygame.FULLSCREEN | pygame.RESIZABLE)
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

tile_image = pygame.image.load('pavement_tile.png').convert_alpha()
background = makeTiledImage( tile_image, LANES_WIDTH, SCREEN_HEIGHT )
left_shoulder = pygame.image.load('left_shoulder.png').convert_alpha()
right_shoulder = pygame.image.load('right_shoulder.png').convert_alpha()
tile_height = 164
 
class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center=(random.randint(40,SCREEN_WIDTH-40),0) 
 
      def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if (self.rect.bottom > SCREEN_HEIGHT):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(30, SCREEN_WIDTH-30), 0)
 
 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (int(SCREEN_WIDTH / 2), SCREEN_HEIGHT - 200)
 
    def move(self):
        pressed_keys = pygame.key.get_pressed()
       #if pressed_keys[K_UP]:
            #self.rect.move_ip(0, -5)
       #if pressed_keys[K_DOWN]:
            #self.rect.move_ip(0,5)
         
        if self.rect.left > 0:
              if pressed_keys[K_LEFT] or pressed_keys[K_a]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
                  self.rect.move_ip(5, 0)
         
P1 = Player()
SPAWNTIME = 6000
last_spawn_tick = 0
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)

tile_placement = TILE_HEIGHT * -1

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 5000)

while True:     
    for event in pygame.event.get():
        if event.type == INC_SPEED:
              SPEED += 2            
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()
    now = pygame.time.get_ticks()
    if now - last_spawn_tick >= SPAWNTIME:
        last_spawn_tick = pygame.time.get_ticks()
        enemy = Enemy()
        enemies.add(enemy)
        all_sprites.add(enemy)
    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(left_shoulder, (0 + OFFSET_WIDTH, 0))
    DISPLAYSURF.blit(background, (LEFT_SHOULDER + OFFSET_WIDTH, tile_placement))
    tile_placement += 5
    if tile_placement > 0:
        tile_placement = TILE_HEIGHT * -1
    DISPLAYSURF.blit(right_shoulder, (LEFT_SHOULDER + OFFSET_WIDTH + LANES_WIDTH, 0))
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(0.5)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, ( int(SCREEN_WIDTH / 2) - 150, int(SCREEN_HEIGHT / 2) - 80) )
        final_score = font.render(f"Final Score: {SCORE}", True, BLACK)
        DISPLAYSURF.blit(final_score, ( int(SCREEN_WIDTH / 2) - 200, int(SCREEN_HEIGHT / 2) + 100) )
        pygame.display.update()
        for entity in all_sprites:
            entity.kill() 
        time.sleep(2)
        pygame.quit()
        sys.exit()  
     
         
    pygame.display.update()
    FramePerSec.tick(FPS)