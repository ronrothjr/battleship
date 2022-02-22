import pygame, sys, os, random, copy, time, numpy
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
PAUSED = False

LANES = int( (SCREEN_WIDTH - SHOULDER_WIDTH) / TILE_WIDTH )
LANES_WIDTH = LANES * TILE_WIDTH - LINE_WIDTH
MAX_ENEMIES = int(LANES * 0.6)
SPEED_INC = (0.5) / MAX_ENEMIES
ENEMY_SPEEDS = [0.65 + (x * SPEED_INC) for x in range(0, MAX_ENEMIES)]
MAX_SPEED = 8
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME | pygame.FULLSCREEN | pygame.RESIZABLE)
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)
paused = font.render("PAUSED", True, BLACK)
 
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

tile_image = pygame.image.load('pavement_tile.png').convert_alpha()
background = makeTiledImage( tile_image, LANES_WIDTH, SCREEN_HEIGHT )
left_shoulder = pygame.image.load('left_shoulder.png').convert_alpha()
right_shoulder = pygame.image.load('right_shoulder.png').convert_alpha()
turn = ''

enemies = pygame.sprite.Group()
hitchers = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("enemy.png")
        self.rect = self.image.get_rect()
        self.lane = self.get_lane()
        x = OFFSET_WIDTH + LEFT_SHOULDER + ( self.lane * TILE_WIDTH ) - int( TILE_WIDTH / 2 ) - int( self.rect.width / 2 )
        self.rect.center=(x,0)
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = ENEMY_SPEEDS.pop(random.randrange(0, len(ENEMY_SPEEDS)))

    def get_lane(self):
        lane = random.randint(1, LANES * 2 - 1)
        while not self.is_lane_empty(lane):
            lane = random.randint(1, LANES * 2 - 1)
        return lane

    def is_lane_empty(self, lane):
        is_empty = True
        for e in enemies:
            if e.lane == lane:
                    return False
        return is_empty

 
    def move(self):
        global SCORE
        self.rect.move_ip(0, int( int(SPEED * 0.65) + int( ( (SPEED / 2) * self.speed ) ) ))
        if (self.rect.bottom > SCREEN_HEIGHT + self.image.get_height()):
            SCORE += 1
            self.rect.top = 0
            self.lane = self.get_lane()
            x = OFFSET_WIDTH + LEFT_SHOULDER + ( self.lane * int( TILE_WIDTH / 2 ) ) - int( TILE_WIDTH / 2 )
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
        up = self.rect.topleft[1] > SCREEN_HEIGHT * 0.55 and (turn == 'boost' or pressed_keys[K_UP] or pressed_keys[K_w])
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
                self.angle += int(SPEED / 5) * 2
        elif right:
            if self.angle > -TURN_RADIUS:
                self.angle -= int(SPEED / 5) * 2
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
        if self.left + x_change < OFFSET_WIDTH + LEFT_SHOULDER:
            x_change = self.left - (OFFSET_WIDTH + LEFT_SHOULDER)
        if self.left + self.rect.width + x_change > SCREEN_WIDTH - RIGHT_SHOULDER:
            x_change = (SCREEN_WIDTH - RIGHT_SHOULDER) - (self.left + self.rect.width)
        self.left += x_change
        self.top += y_change
        self.rect.move_ip(x_change, y_change)
        if not up and not down and not left and not right:
            turn = ''
            if self.angle != 0 and self.angle <=TURN_RADIUS and self.angle >= -TURN_RADIUS:
                self.angle += -int(SPEED / 5) * 2 if self.angle > 0 else int(SPEED / 5) * 2
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


class Hitchhiker(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.id = random.choice([1,2,3,4,5,6])
        self.image = pygame.image.load(f"hitchhiker{self.id}.png")
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        sides = []
        left = OFFSET_WIDTH + int(LEFT_SHOULDER / 2)
        sides.append(left)
        right = OFFSET_WIDTH + LEFT_SHOULDER + LANES_WIDTH + int(RIGHT_SHOULDER / 2)
        sides.append(right)
        side = random.choice(sides)
        if side == left:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect.center=(side, SCREEN_HEIGHT * -0.05)
        
    def move(self):
        self.rect.move_ip(0, int(SPEED / 2))
        if (self.rect.bottom > SCREEN_HEIGHT + self.image.get_height()):
            self.kill()

    def play(self):
        pygame.mixer.Sound(f'hitchhiker{self.id}.wav').play()

         
P1 = Player()
all_sprites.add(P1)
now = pygame.time.get_ticks()
SPAWN_ENEMY = 10000
INC_SPEED = 15000
SPAWN_HITCHHIKER = 5000
LAST_SPAWN_ENEMY = now
LAST_INC_SPEED = now
LAST_SPAWN_HITCHHIKER = now

tile_placement = TILE_HEIGHT * -1

pygame.mouse.set_pos((int(SCREEN_WIDTH * 0.8), int(SCREEN_HEIGHT * 0.5)))

while True:
    now = pygame.time.get_ticks()
    for event in pygame.event.get():
        if PAUSED:
            if event.type in [KEYDOWN, MOUSEBUTTONDOWN, MOUSEMOTION]:
                PAUSED = False
                LAST_SPAWN_ENEMY = now - LAST_SPAWN_ENEMY
                LAST_INC_SPEED = now - LAST_INC_SPEED
                LAST_SPAWN_HITCHHIKER = now - LAST_SPAWN_HITCHHIKER
            else:
                continue
        elif not PAUSED and event.type == KEYDOWN and event.key == K_p:
            PAUSED = True
            LAST_SPAWN_ENEMY = now - LAST_SPAWN_ENEMY
            LAST_INC_SPEED = now - LAST_INC_SPEED
            LAST_SPAWN_HITCHHIKER = now - LAST_SPAWN_HITCHHIKER
            continue
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN or event.type == MOUSEMOTION:
            pos = event.pos
            x = pos[0] / SCREEN_WIDTH
            click = pygame.mouse.get_pressed()
            turn = 'boost' if click[2] or x < 0.3 else ('left' if x < 0.45 else ('boost' if x > 0.7 else ('right' if x > 0.55 else '')))
        if event.type == MOUSEBUTTONUP:
            turn = ''

    if PAUSED:
        DISPLAYSURF.blit(paused, ( int(SCREEN_WIDTH / 2) - 150, int(SCREEN_HEIGHT / 2) - 80) )
    
    else:

        if now - LAST_INC_SPEED >= INC_SPEED and SPEED < MAX_SPEED:
            LAST_INC_SPEED = now
            SPEED += 2
        if now - LAST_SPAWN_HITCHHIKER >= SPAWN_HITCHHIKER:
            LAST_SPAWN_HITCHHIKER = now
            hitcher = Hitchhiker()
            hitchers.add(hitcher)
            all_sprites.add(hitcher)
        if now - LAST_SPAWN_ENEMY >= SPAWN_ENEMY and enemies.__len__() < MAX_ENEMIES:
            LAST_SPAWN_ENEMY = now
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
        speed_spawn = font_small.render(f'{str(now - LAST_INC_SPEED)}', True, BLACK)
        DISPLAYSURF.blit(speed_spawn, (110,35))
        inc_speed = font_small.render(f'{str(INC_SPEED)}', True, BLACK)
        DISPLAYSURF.blit(inc_speed, (210,35))
        count = font_small.render(str(enemies.__len__()), True, BLACK)
        DISPLAYSURF.blit(count, (10,60))
        enemy_spawn = font_small.render(f'{str(now - LAST_SPAWN_ENEMY)}', True, BLACK)
        DISPLAYSURF.blit(enemy_spawn, (110,60))
        spawn_enemy = font_small.render(f'{str(SPAWN_ENEMY)}', True, BLACK)
        DISPLAYSURF.blit(spawn_enemy, (210,60))
        hitch_spawn = font_small.render(f'{str(now - LAST_SPAWN_HITCHHIKER)}', True, BLACK)
        DISPLAYSURF.blit(hitch_spawn, (110,95))
        hitcher = font_small.render(f'{str(SPAWN_HITCHHIKER)}', True, BLACK)
        DISPLAYSURF.blit(hitcher, (210,95))
        boost_left = font.render('boost |', True, BLACK)
        DISPLAYSURF.blit(boost_left, (int(SCREEN_WIDTH * 0.15), SCREEN_HEIGHT * 0.85))
        left = font.render('<', True, BLACK)
        DISPLAYSURF.blit(left, (int(SCREEN_WIDTH * 0.40), SCREEN_HEIGHT * 0.85))
        right = font.render('>', True, BLACK)
        DISPLAYSURF.blit(right, (int(SCREEN_WIDTH * 0.57), SCREEN_HEIGHT * 0.85))
        boost_right = font.render('| boost', True, BLACK)
        DISPLAYSURF.blit(boost_right, (int(SCREEN_WIDTH * 0.70), SCREEN_HEIGHT * 0.85))
        
        for e in enemies:
            squished = pygame.sprite.spritecollide(e, hitchers, True, pygame.sprite.collide_mask)
            if squished:
                for h in squished:
                    h.kill()
        
        hitched = pygame.sprite.spritecollide(P1, hitchers, True, pygame.sprite.collide_mask)
        if hitched:
            for h in hitched:
                h.play()
                SCORE += 5

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
