import pygame, os, time
from player import Player
from hitchhiker import Hitchhiker
from enemy import Enemy
from settings import Settings

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


class Hitcher:

    def __init__(self, settings: Settings):
        self.settings: Settings = settings
        self.on_init()

    def on_init(self):
        self.P1 = Player(self.settings)
        self.settings.all_sprites.add(self.P1)
        now = self.settings.pg.time.get_ticks()
        self.LAST_SPAWN_ENEMY = now
        self.LAST_INC_SPEED = now
        self.LAST_SPAWN_HITCHHIKER = now
        self.tile_placement = self.settings.TILE_HEIGHT * -1
        self.settings.pg.mouse.set_pos((int(self.settings.SCREEN_WIDTH * 0.5), int(self.settings.SCREEN_HEIGHT * 0.8)))

    def on_start(self):
        self.settings.pg.mixer.Sound('traffic.wav').play()

    def on_pause(self, now):
        self.LAST_SPAWN_ENEMY = now - self.LAST_SPAWN_ENEMY
        self.LAST_INC_SPEED = now - self.LAST_INC_SPEED
        self.LAST_SPAWN_HITCHHIKER = now - self.LAST_SPAWN_HITCHHIKER

    def on_unpause(self, now):
        self.LAST_SPAWN_ENEMY = now - self.LAST_SPAWN_ENEMY
        self.LAST_INC_SPEED = now - self.LAST_INC_SPEED
        self.LAST_SPAWN_HITCHHIKER = now - self.LAST_SPAWN_HITCHHIKER

    def on_loop(self, now, move):
        keep_looping = True
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
            keep_looping = False
        return keep_looping

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
