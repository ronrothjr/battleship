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
TURN_RADIUS = 30
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
turn = ''
 
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
 
    def move(self, turn: str=''):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if (self.rect.bottom > SCREEN_HEIGHT + self.image.get_height()):
            SCORE += 1
            self.rect.top = 0
            lane = self.get_lane()
            x = OFFSET_WIDTH + LEFT_SHOULDER + ( lane * int( TILE_WIDTH / 2 ) ) - int( TILE_WIDTH / 2 )
            self.rect.center = (x, 0)
        return turn


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("player.png")
        self.original_image = copy.copy(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT * 0.8))
        self.angle = 0
        self.boost = 0
        self.boosting = False
        self.recharge = 0
        self.left = self.rect.topleft[0]
        self.top = self.rect.topleft[1]
        self.mask = pygame.mask.from_surface(self.image)
        self.turning = None

    def move(self, turn: str=''):
        pressed_keys = pygame.key.get_pressed()
        up = self.rect.topleft[1] > SCREEN_HEIGHT * 0.55 and (pressed_keys[K_UP] or pressed_keys[K_w])
        not_bottom = self.rect.bottomright[1] < SCREEN_HEIGHT * 0.8 + int( self.rect.height / 2 )
        down = not_bottom and (pressed_keys[K_SPACE])
        left = self.rect.left > OFFSET_WIDTH + LEFT_SHOULDER and (turn == 'left' or pressed_keys[K_LEFT] or pressed_keys[K_a])
        right = self.rect.right < SCREEN_WIDTH - RIGHT_SHOULDER and (turn == 'right' or pressed_keys[K_RIGHT] or pressed_keys[K_d])
        x_change = 0
        y_change = 0
        if up:
            if (self.recharge == 0 or self.boosting):
                if not self.boosting:
                    self.recharge = 180
                    self.boosting = True
                if self.boost < SPEED:
                    if self.boost == 0:
                        pygame.mixer.Sound('boost.wav').play()
                    self.boost += int(SPEED / 5)
                else:
                    self.boosting = False
            turn = 'up'
        elif down:
            y_change = int(SPEED / 2)
            turn = 'down'
        if left:
            if self.angle < TURN_RADIUS:
                self.angle += 1
        elif right:
            if self.angle > -TURN_RADIUS:
                self.angle -= 1
        if self.angle != 0:
            self.turning = 'right' if self.angle > -TURN_RADIUS else 'left'
            x_change = int((SPEED + self.boost) / 3 * (self.angle / TURN_RADIUS * -1))
            self.set_rotation()
        if self.boost > 0:
            y_change -= self.boost
            if not up:
                self.boost -= int(SPEED / 5)
        elif not_bottom:
            y_change += int(SPEED / 5)
        if self.recharge > 0:
            self.recharge -= int(SPEED / 5)
        self.left += x_change
        self.top += y_change
        self.rect.move_ip(x_change, y_change)
        if not up and not down and not left and not right:
            turn = ''
            if self.angle != 0 and self.angle <=TURN_RADIUS and self.angle >= -TURN_RADIUS:
                self.angle += -1 if self.angle > 0 else 1
                self.set_rotation()
        return turn

    def set_rotation(self):
        self.image = copy.copy(self.original_image)
        self.image, self.rect = self.blitRotateCenter(self.image, (self.left, self.top), self.angle)
        self.mask = pygame.mask.from_surface(self.image)

    def blitRotateCenter(self, image, topleft, angle):
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)
        return rotated_image, new_rect
    
    def reset_rotation(self):
        if self.original_image:
            self.image = copy.copy(self.original_image)
            self.rect = self.image.get_rect(center = self.image.get_rect(topleft = (self.rect.x, self.top + int( self.rect.height / 2 ))).center)
            self.mask = pygame.mask.from_surface(self.image)
            self.original_image = None
            self.turning = None

         
P1 = Player()
SPAWNTIME = 10000
last_spawn_tick = 0
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)

tile_placement = TILE_HEIGHT * -1


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

    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        if entity == P1:
            turn = entity.move(turn)
        else:
            entity.move()

    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))
    speed = font_small.render(f'{str((SPEED + P1.boost) * 2)} mph', True, BLACK)
    DISPLAYSURF.blit(speed, (10,35))
    count = font_small.render(str(enemies.__len__()), True, BLACK)
    DISPLAYSURF.blit(count, (10,60))
    # turning = font_small.render(str(turn), True, BLACK)
    # DISPLAYSURF.blit(turning, (10,100))
    # position = font_small.render(f'{str(P1.rect.topleft[1])},{str(P1.rect.left)},{str(P1.rect.bottomright[1])},{str(P1.rect.right)}', True, BLACK)
    # DISPLAYSURF.blit(position, (40,10))
    # up = font_small.render(f'{str(SCREEN_HEIGHT * 0.55)}', True, BLACK)
    # DISPLAYSURF.blit(up, (40,35))
    # down = font_small.render(f'{str(SCREEN_HEIGHT * 0.85)}', True, BLACK)
    # DISPLAYSURF.blit(down, (40,60))
    # angle = font_small.render(f'{str(P1.angle)}', True, BLACK)
    # DISPLAYSURF.blit(angle, (40,100))

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