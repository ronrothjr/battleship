import pygame, sys, os, random, copy, time
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
LINE_WIDTH = 18
SHOULDER_WIDTH = LEFT_SHOULDER + RIGHT_SHOULDER
TILE_WIDTH = 134
TILE_HEIGHT = 164
OFFSET_WIDTH = int( ( ( SCREEN_WIDTH - SHOULDER_WIDTH ) % TILE_WIDTH ) / 2 ) + ( LINE_WIDTH / 2 )
SPEED = 5
SCORE = 0

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)
 
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

def blitRotateCenter(image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)
    return rotated_image, new_rect

def draw_ellipse_angle(surface, color, rect, angle, width=0):
    target_rect = pygame.Rect(rect)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.ellipse(shape_surf, color, (0, 0, *target_rect.size), width)
    rotated_surf = pygame.transform.rotate(shape_surf, angle)
    surface.blit(rotated_surf, rotated_surf.get_rect(center = target_rect.center))

LANES = int( (SCREEN_WIDTH - SHOULDER_WIDTH) / TILE_WIDTH )
LANES_WIDTH = LANES * TILE_WIDTH - LINE_WIDTH
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
        lane = self.get_lane()
        x = OFFSET_WIDTH + LEFT_SHOULDER + ( lane * TILE_WIDTH ) - int( TILE_WIDTH / 2 )
        self.rect.center=(x,0)
        self.mask = pygame.mask.from_surface(self.image)

    def get_lane(self):
        return random.randint(1, LANES * 2)
 
    def move(self, pos: str=''):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if (self.rect.bottom > SCREEN_HEIGHT + self.image.get_height()):
            SCORE += 1
            self.rect.top = 0
            lane = self.get_lane()
            x = OFFSET_WIDTH + LEFT_SHOULDER + ( lane * int( TILE_WIDTH / 2 ) ) - int( TILE_WIDTH / 2 )
            self.rect.center = (x, 0)
 
 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT * 0.8))
        self.mask = pygame.mask.from_surface(self.image)
        self.turning = None
        self.original_image = None
        self.original_rect = None
 
    def move(self, pos: str=''):
        pressed_keys = pygame.key.get_pressed()
       #if pressed_keys[K_UP]:
            #self.rect.move_ip(0, -5)
       #if pressed_keys[K_DOWN]:
            #self.rect.move_ip(0,5)
        left = self.rect.left > OFFSET_WIDTH + LEFT_SHOULDER and (pos == 'left' or pressed_keys[K_LEFT] or pressed_keys[K_a])
        right = self.rect.right < SCREEN_WIDTH - RIGHT_SHOULDER and (pos == 'right' or pressed_keys[K_RIGHT] or pressed_keys[K_d])
        if left:
            if self.original_image and self.turning == 'right':
                self.reset_rotation()
            if not self.original_image:
                self.set_rotation('left', 15)
            self.rect.move_ip(int(SPEED / 2) * -1, 0)
        elif right:
            if self.original_image and self.turning == 'left':
                self.reset_rotation()
            if not self.original_image:
                self.set_rotation('right', -15)
            self.rect.move_ip(int(SPEED / 2), 0)
        if not left and not right:
            self.reset_rotation()

    def set_rotation(self, turn, angle):
        self.turning = turn
        self.original_image = copy.copy(self.image)
        self.original_rect = copy.copy(self.rect)
        self.image, self.rect = blitRotateCenter(self.image, (self.rect.x, self.rect.y), angle)
        self.mask = pygame.mask.from_surface(self.image)
    
    def reset_rotation(self):
        if self.original_image:
            self.image = copy.copy(self.original_image)
            height = (SCREEN_HEIGHT * 0.8) - int(self.image.get_height() / 2)
            self.rect = self.image.get_rect(center = self.image.get_rect(topleft = (self.rect.x, height)).center)
            self.mask = pygame.mask.from_surface(self.image)
            self.original_image = None
            self.original_rect = None
            self.turning = None

         
P1 = Player()
SPAWNTIME = 10000
last_spawn_tick = 0
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)

tile_placement = TILE_HEIGHT * -1

turn = ''

INC_SPEED = pygame.USEREVENT + 1
MAX_ENEMIES = 20
MAX_SPEED = 30
pygame.time.set_timer(INC_SPEED, 15000)

while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED and SPEED < MAX_SPEED:
              SPEED += 2            
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN or event.type == MOUSEMOTION:
            pos = event.pos
            x = pos[0] / SCREEN_WIDTH
            turn = 'left' if x < 0.4 else ('right' if x > 0.6 else '')
        if event.type == MOUSEBUTTONUP:
            turn = ''

    now = pygame.time.get_ticks()
    if now - last_spawn_tick >= SPAWNTIME and enemies.__len__() < MAX_ENEMIES:
        last_spawn_tick = pygame.time.get_ticks()
        enemy = Enemy()
        enemies.add(enemy)
        all_sprites.add(enemy)

    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(left_shoulder, (0 + OFFSET_WIDTH, 0))
    DISPLAYSURF.blit(background, (LEFT_SHOULDER + OFFSET_WIDTH, tile_placement))
    tile_placement += int(SPEED / 2)
    if tile_placement > 0:
        tile_placement = TILE_HEIGHT * -1
    DISPLAYSURF.blit(right_shoulder, (LEFT_SHOULDER + OFFSET_WIDTH + LANES_WIDTH, 0))

    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))
    speed = font_small.render(str(SPEED), True, BLACK)
    DISPLAYSURF.blit(speed, (10,35))
    count = font_small.render(str(enemies.__len__()), True, BLACK)
    DISPLAYSURF.blit(count, (10,60))
    turning = font_small.render(str(turn), True, BLACK)
    DISPLAYSURF.blit(turning, (10,100))
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move(turn)

    if pygame.sprite.spritecollide(P1, enemies, False, pygame.sprite.collide_mask):
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