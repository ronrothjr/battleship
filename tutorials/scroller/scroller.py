import pygame, sys, os, random, copy, time
from pygame.locals import *

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


class Player(pygame.sprite.Sprite):
    def __init__(self, settings: Settings):
        super().__init__()
        self.settings: Settings = settings
        self.image = self.settings.pg.image.load("player.png")
        self.original_image = copy.copy(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (int(self.settings.SCREEN_WIDTH / 2), int(self.settings.SCREEN_HEIGHT * 0.8))
        self.angle = 0
        self.boost = 0
        self.boosting = False
        self.recharge = 0
        self.left = self.rect.topleft[0]
        self.top = self.rect.topleft[1]
        self.mask = self.settings.pg.mask.from_surface(self.image)
        self.turning = None

    def move(self, move: str=''):
        pressed_keys = self.settings.pg.key.get_pressed()
        up = self.rect.topleft[1] > self.settings.SCREEN_HEIGHT * 0.55 and (move == 'boost' or pressed_keys[K_UP] or pressed_keys[K_w])
        not_bottom = self.rect.bottomright[1] < self.settings.SCREEN_HEIGHT * 0.8 + int( self.rect.height / 2 )
        down = not_bottom and (pressed_keys[K_SPACE])
        left = self.rect.left > self.settings.MARGIN + self.settings.LEFT_SHOULDER and (move == 'left' or pressed_keys[K_LEFT] or pressed_keys[K_a])
        right = self.rect.right < self.settings.SCREEN_WIDTH - self.settings.RIGHT_SHOULDER and (move == 'right' or pressed_keys[K_RIGHT] or pressed_keys[K_d])
        x_change = 0
        y_change = 0

        if up:
            if (self.recharge == 0 or self.boosting):
                if not self.boosting:
                    self.recharge = 180
                    self.boosting = True
                if self.boost < self.settings.SPEED:
                    if self.boost == 0:
                        self.settings.pg.mixer.Sound('boost.wav').play()
                    self.boost += int(self.settings.SPEED / 5)
                else:
                    self.boosting = False
            move = 'up'

        elif down:
            y_change = int(self.settings.SPEED / 2)
            move = 'down'

        if left:
            if self.angle < self.settings.TURN_RADIUS:
                self.angle += int(self.settings.SPEED / 5) * 2

        elif right:
            if self.angle > -self.settings.TURN_RADIUS:
                self.angle -= int(self.settings.SPEED / 5) * 2

        if self.angle != 0:
            self.turning = 'right' if self.angle > -self.settings.TURN_RADIUS else 'left'
            x_change = int((self.settings.SPEED + self.boost) / 3 * (self.angle / self.settings.TURN_RADIUS * -1))
            self.set_rotation()

        if self.boost > 0:
            y_change -= self.boost
            if not up:
                self.boost -= int(self.settings.SPEED / 5)
        elif not_bottom:
            y_change += int(self.settings.SPEED / 5)

        if self.recharge > 0:
            self.recharge -= int(self.settings.SPEED / 5)

        if self.left + x_change < self.settings.MARGIN + self.settings.LEFT_SHOULDER:
            x_change = self.left - (self.settings.MARGIN + self.settings.LEFT_SHOULDER)
        if self.left + self.rect.width + x_change > self.settings.SCREEN_WIDTH - self.settings.RIGHT_SHOULDER:
            x_change = (self.settings.SCREEN_WIDTH - self.settings.RIGHT_SHOULDER) - (self.left + self.rect.width)
        self.left += x_change
        self.top += y_change
        self.rect.move_ip(x_change, y_change)
        if not up and not down and not left and not right:
            move = ''
            if self.angle != 0 and self.angle <=self.settings.TURN_RADIUS and self.angle >= -self.settings.TURN_RADIUS:
                self.angle += -int(self.settings.SPEED / 5) * 2 if self.angle > 0 else int(self.settings.SPEED / 5) * 2
                self.set_rotation()
        return move

    def set_rotation(self):
        self.image = copy.copy(self.original_image)
        self.image, self.rect = self.blitRotateCenter(self.image, (self.left, self.top), self.angle)
        self.mask = self.settings.pg.mask.from_surface(self.image)

    def blitRotateCenter(self, image, topleft, angle):
        rotated_image = self.settings.pg.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)
        return rotated_image, new_rect


class Hitchhiker(pygame.sprite.Sprite):
    def __init__(self, settings: Settings):
        super().__init__()
        self.settings: Settings = settings
        self.id = random.choice([1,2,3,4,5,6])
        self.image = self.settings.pg.image.load(f"hitchhiker{self.id}.png")
        self.rect = self.image.get_rect()
        self.mask = self.settings.pg.mask.from_surface(self.image)
        sides = []
        left = self.settings.MARGIN + int(self.settings.LEFT_SHOULDER / 2)
        sides.append(left)
        right = self.settings.MARGIN + self.settings.LEFT_SHOULDER + self.settings.LANES_WIDTH + int(self.settings.RIGHT_SHOULDER / 2)
        sides.append(right)
        side = random.choice(sides)
        if side == left:
            self.image = self.settings.pg.transform.flip(self.image, True, False)
        self.rect.center=(side, self.settings.SCREEN_HEIGHT * -0.05)
        
    def move(self):
        self.rect.move_ip(0, int(self.settings.SPEED / 2))
        if (self.rect.bottom > self.settings.SCREEN_HEIGHT + self.image.get_height()):
            self.kill()

    def play(self, reaction: str):
        self.settings.pg.mixer.Sound(f'{reaction}{self.id}.wav').play()


class Hitcher:

    def __init__(self, settings: Settings):
        self.settings: Settings = settings
        self.on_init()

    def on_init(self):
        self.framePerSec = self.settings.pg.time.Clock()
        self.PAUSED = False
        self.P1 = Player(self.settings)
        self.settings.all_sprites.add(self.P1)
        now = self.settings.pg.time.get_ticks()
        self.LAST_SPAWN_ENEMY = now
        self.LAST_INC_SPEED = now
        self.LAST_SPAWN_HITCHHIKER = now
        self.tile_placement = self.settings.TILE_HEIGHT * -1
        self.settings.pg.mouse.set_pos((int(self.settings.SCREEN_WIDTH * 0.5), int(self.settings.SCREEN_HEIGHT * 0.8)))

    def game_loop(self):
        self.settings.pg.mixer.Sound('traffic.wav').play()
        while True:
            now = self.settings.pg.time.get_ticks()
            for event in self.settings.pg.event.get():
                self.handle_pause(event, now)
                if self.is_quitting(event):
                    self.settings.pg.quit()
                    sys.exit()
                move = self.get_move(event)
            if not self.PAUSED:
                self.handle_speed(now)
                self.spawn_hitchhikers(now)
                self.spawn_enemies(now)
                self.scroll_pavement()
                move = self.move_all_sprites(move)
                self.squish_hitchhikers()
                self.pick_up_hitchhikers()
                self.display_info()
                if self.is_crash():
                    self.handle_crash()
                    self.settings.pg.quit()
                    sys.exit()
            self.settings.pg.display.update()
            self.framePerSec.tick(self.settings.FPS)

    def handle_pause(self, event, now):
        if self.PAUSED:
            if self.any_key(event):
                self.unpause(now)
        elif not self.PAUSED:
            y = self.get_y(event)
            if self.is_paused(y, event):
                self.pause(now)
        if self.PAUSED:
            self.settings.DISPLAYSURF.blit(self.settings.paused, ( int(self.settings.SCREEN_WIDTH / 2) - 150, int(self.settings.SCREEN_HEIGHT / 2) - 80) )

    def is_paused(self, y, event):
        return y < 0.3 or event.type == self.settings.pg.KEYDOWN and event.key == self.settings.pg.K_p

    def is_quitting(self, event):
        return event.type == QUIT or event.type == self.settings.pg.KEYDOWN and event.key == self.settings.pg.K_ESCAPE
        
    def any_key(self, event):
        return event.type in [self.settings.pg.KEYDOWN, self.settings.pg.MOUSEBUTTONDOWN, self.settings.pg.MOUSEMOTION]

    def pause(self, now):
        self.PAUSED = True
        self.LAST_SPAWN_ENEMY = now - self.LAST_SPAWN_ENEMY
        self.LAST_INC_SPEED = now - self.LAST_INC_SPEED
        self.LAST_SPAWN_HITCHHIKER = now - self.LAST_SPAWN_HITCHHIKER

    def unpause(self, now):
        self.PAUSED = False
        self.LAST_SPAWN_ENEMY = now - self.LAST_SPAWN_ENEMY
        self.LAST_INC_SPEED = now - self.LAST_INC_SPEED
        self.LAST_SPAWN_HITCHHIKER = now - self.LAST_SPAWN_HITCHHIKER

    def get_y(self, event):
        y = 1
        if event.type == self.settings.pg.MOUSEBUTTONDOWN or event.type == self.settings.pg.MOUSEMOTION:
            pos = event.pos
            y = pos[1] / self.settings.SCREEN_HEIGHT
        return y

    def get_move(self, event):
        if event.type == self.settings.pg.MOUSEBUTTONDOWN or event.type == self.settings.pg.MOUSEMOTION:
            pos = event.pos
            x = pos[0] / self.settings.SCREEN_WIDTH
            click = self.settings.pg.mouse.get_pressed()
            move = 'boost' if click[2] or x < 0.3 else ('left' if x < 0.45 else ('boost' if x > 0.7 else ('right' if x > 0.55 else '')))
            if event.type == self.settings.pg.MOUSEBUTTONUP:
                move = ''
            return move

    def handle_speed(self, now):
        if now - self.LAST_INC_SPEED >= self.settings.INC_SPEED and self.settings.SPEED < self.settings.MAX_SPEED:
            self.LAST_INC_SPEED = now
            self.settings.SPEED += 2

    def spawn_hitchhikers(self, now):
        if now - self.LAST_SPAWN_HITCHHIKER >= self.settings.SPAWN_HITCHHIKER:
            self.LAST_SPAWN_HITCHHIKER = now
            hitcher = Hitchhiker(self.settings)
            self.settings.hitchers.add(hitcher)
            self.settings.all_sprites.add(hitcher)

    def spawn_enemies(self, now):
        if now - self.LAST_SPAWN_ENEMY >= self.settings.SPAWN_ENEMY and self.settings.enemies.__len__() < self.settings.MAX_ENEMIES:
            self.LAST_SPAWN_ENEMY = now
            enemy = Enemy(self.settings)
            self.settings.enemies.add(enemy)
            self.settings.all_sprites.add(enemy)

    def scroll_pavement(self):
        self.settings.DISPLAYSURF.fill(self.settings.WHITE)
        self.settings.DISPLAYSURF.blit(self.settings.left_shoulder, (0 + self.settings.MARGIN, 0))
        self.settings.DISPLAYSURF.blit(self.settings.background, (self.settings.LEFT_SHOULDER + self.settings.MARGIN, self.tile_placement))
        self.tile_placement += int(self.settings.SPEED / 2)
        if self.tile_placement > 0:
            self.tile_placement = self.settings.TILE_HEIGHT * -1
        self.settings.DISPLAYSURF.blit(self.settings.right_shoulder, (self.settings.LEFT_SHOULDER + self.settings.MARGIN + self.settings.LANES_WIDTH, 0))

    def move_all_sprites(self, move):
        for entity in self.settings.all_sprites:
              self.settings.DISPLAYSURF.blit(entity.image, entity.rect)
              if entity == self.P1:
                    move = entity.move(move)
              else:
                    entity.move()
        return move

    def display_info(self):
        scores = self.settings.font_small.render(str(self.settings.SCORE), True, self.settings.BLACK)
        self.settings.DISPLAYSURF.blit(scores, (10,10))
        speed = self.settings.font_small.render(f'{str((self.settings.SPEED + self.P1.boost) * 2)} mph', True, self.settings.BLACK)
        self.settings.DISPLAYSURF.blit(speed, (10,35))
        count = self.settings.font_small.render(str(self.settings.enemies.__len__()), True, self.settings.BLACK)
        self.settings.DISPLAYSURF.blit(count, (10,60))
        boost_left = self.settings.font.render('boost |', True, self.settings.BLACK)
        self.settings.DISPLAYSURF.blit(boost_left, (int(self.settings.SCREEN_WIDTH * 0.15), self.settings.SCREEN_HEIGHT * 0.85))
        left = self.settings.font.render('<', True, self.settings.BLACK)
        self.settings.DISPLAYSURF.blit(left, (int(self.settings.SCREEN_WIDTH * 0.40), self.settings.SCREEN_HEIGHT * 0.85))
        right = self.settings.font.render('>', True, self.settings.BLACK)
        self.settings.DISPLAYSURF.blit(right, (int(self.settings.SCREEN_WIDTH * 0.57), self.settings.SCREEN_HEIGHT * 0.85))
        boost_right = self.settings.font.render('| boost', True, self.settings.BLACK)
        self.settings.DISPLAYSURF.blit(boost_right, (int(self.settings.SCREEN_WIDTH * 0.70), self.settings.SCREEN_HEIGHT * 0.85))

    def squish_hitchhikers(self):
        for e in self.settings.enemies:
            squished = self.settings.pg.sprite.spritecollide(e, self.settings.hitchers, True, self.settings.pg.sprite.collide_mask)
            if squished:
                for h in squished:
                    h.play('pain')
                    h.kill()

    def pick_up_hitchhikers(self):
        hitched = self.settings.pg.sprite.spritecollide(self.P1, self.settings.hitchers, True, self.settings.pg.sprite.collide_mask)
        if hitched:
            for h in hitched:
                h.play('hitchhiker')
                self.settings.SCORE += 5

    def is_crash(self):
        return self.settings.pg.sprite.spritecollide(self.P1, self.settings.enemies, False, self.settings.pg.sprite.collide_mask)

    def handle_crash(self):
        self.settings.pg.mixer.Sound('crash.wav').play()
        time.sleep(0.5)
        self.settings.DISPLAYSURF.fill(self.settings.RED)
        self.settings.DISPLAYSURF.blit(self.settings.game_over, ( int(self.settings.SCREEN_WIDTH / 2) - 150, int(self.settings.SCREEN_HEIGHT / 2) - 80) )
        final_score = self.settings.font.render(f"Final Score: {self.settings.SCORE}", True, self.settings.BLACK)
        self.settings.DISPLAYSURF.blit(final_score, ( int(self.settings.SCREEN_WIDTH / 2) - 200, int(self.settings.SCREEN_HEIGHT / 2) + 100) )
        self.settings.pg.display.update()
        for entity in self.settings.all_sprites:
            entity.kill() 
        time.sleep(2)


if __name__ == '__main__':
    Hitcher(Settings(pygame)).game_loop()
