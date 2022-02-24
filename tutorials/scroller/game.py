import time, copy
from player import Player
from hitchhiker import Hitchhiker
from enemy import Enemy
from settings import Settings


class Game:

    def __init__(self, settings: Settings):
        self.settings: Settings = settings
        self.on_init()

    def on_init(self):
        self.bg_placement = self.settings.tile_height * -1
        self.settings.pg.mouse.set_pos((int(self.settings.screen_width * 0.5), int(self.settings.screen_height * 0.8)))
        self.left_shoulder = None
        self.right_shoulder = None

    def on_start(self, level: dict):
        self.settings.set_game_difficulty(level)
        self.left_shoulder = self.settings.scale_image(copy.copy(self.settings.left_shoulder))
        self.right_shoulder = self.settings.scale_image(copy.copy(self.settings.right_shoulder))
        self.settings.display.fill(self.settings.gray)
        instructions = self.settings.font_medium.render(f"Rescue {self.settings.rescue} hitchhikers before {self.settings.squish} get{'s' if self.settings.squish == 1 else ''} squished", True, self.settings.black)
        self.settings.display.blit(instructions, ( int(self.settings.screen_width / 2) - 400, int(self.settings.screen_height / 2) - 80) )
        self.settings.pg.display.update()
        time.sleep(2)
        self.settings.pg.mixer.stop()
        self.traffic = self.settings.pg.mixer.Sound(self.settings.get_path('sounds', 'traffic.wav'))
        self.traffic.play(fade_ms=5000)
        self.P1 = Player(self.settings)
        self.settings.all_sprites.add(self.P1)
        now = self.settings.pg.time.get_ticks()
        self.last_spawn_enemy = now
        self.last_inc_speed = now
        self.last_spawn_hitchhiker = now

    def on_pause(self, now):
        self.last_spawn_enemy = now - self.last_spawn_enemy
        self.last_inc_speed = now - self.last_inc_speed
        self.last_spawn_hitchhiker = now - self.last_spawn_hitchhiker
        self.settings.pg.mixer.pause()

    def on_unpause(self, now):
        self.last_spawn_enemy = now - self.last_spawn_enemy
        self.last_inc_speed = now - self.last_inc_speed
        self.last_spawn_hitchhiker = now - self.last_spawn_hitchhiker
        self.settings.pg.mixer.unpause()

    def on_loop(self, now, move):
        alive = True
        leveled = False
        self.handle_speed(now)
        self.spawn_hitchhikers(now)
        self.spawn_enemies(now)
        self.scroll_pavement()
        move = self.move_all_sprites(move)
        self.squish_hitchhikers()
        self.pick_up_hitchhikers()
        self.display_info()
        if self.squished():
            self.handle_squished()
            alive = False
        elif self.level_up():
            self.handle_level_up()
            leveled = True
        elif self.is_crash():
            self.handle_crash()
            alive = False
        return {'alive': alive, 'leveled': leveled}

    def get_move(self, event):
        move = ''
        is_mouse = event.type == self.settings.pg.MOUSEBUTTONDOWN or event.type == self.settings.pg.MOUSEMOTION
        is_finger = event.type in [self.settings.pg.FINGERDOWN, self.settings.pg.FINGERMOTION]
        is_move = is_mouse or is_finger
        is_stop_move = event.type == self.settings.pg.MOUSEBUTTONUP or event.type == self.settings.pg.KEYUP or event.type == self.settings.pg.FINGERUP
        if is_stop_move:
            move = ''
        elif is_move:
            pos = event.x if is_finger else event.pos[0] / self.settings.screen_width
            click = self.settings.pg.mouse.get_pressed()
            if pos < 0.3 or pos > 0.7 or (is_mouse and click[2]):
                move = 'boost'
            elif pos < 0.45:
                move = 'left'
            elif pos > 0.55:
                move = 'right'
            else:
                move = ''
        return move

    def handle_speed(self, now):
        is_time_to_increase_speed = now - self.last_inc_speed >= self.settings.inc_speed and self.settings.speed < self.settings.max_speed
        if is_time_to_increase_speed:
            self.last_inc_speed = now
            self.settings.speed += 1

    def spawn_hitchhikers(self, now):
        is_time_to_spawn_hitchhikers = now - self.last_spawn_hitchhiker >= self.settings.spawn_hitchhiker
        if is_time_to_spawn_hitchhikers:
            self.last_spawn_hitchhiker = now
            hitcher = Hitchhiker(self.settings)
            self.settings.hitchers.add(hitcher)
            self.settings.all_sprites.add(hitcher)

    def spawn_enemies(self, now):
        is_time_to_spawn = now - self.last_spawn_enemy >= self.settings.spawn_enemy and self.settings.enemies.__len__() < self.settings.max_enemies
        if is_time_to_spawn:
            self.last_spawn_enemy = now
            enemy = Enemy(self.settings)
            self.settings.enemies.add(enemy)
            self.settings.all_sprites.add(enemy)

    def scroll_pavement(self):
        self.settings.display.fill(self.settings.gray)
        self.settings.display.blit(self.left_shoulder, (0 + self.settings.margin, 0))
        self.settings.display.blit(self.settings.background, (self.settings.left_edge, self.bg_placement))
        self.bg_placement += int(self.settings.speed / 2)
        if self.bg_placement > 0:
            self.bg_placement = self.settings.tile_height * -1
        self.settings.display.blit(self.right_shoulder, (self.settings.right_edge, 0))

    def move_all_sprites(self, move):
        for entity in self.settings.all_sprites:
              self.settings.display.blit(entity.image, entity.rect)
              if entity == self.P1:
                    move = entity.move(move)
              else:
                    entity.move()
        return move

    def display_info(self):
        speed = self.settings.font_small.render(f'{str((self.settings.speed + self.P1.boost) * 2)} mph', True, self.settings.white)
        self.settings.display.blit(speed, (10,10))
        scores = self.settings.font_small.render(f'{str(self.settings.rescued)} rescued', True, self.settings.white)
        self.settings.display.blit(scores, (10,35))
        count = self.settings.font_small.render(f'{str(self.settings.enemies.__len__())} enemies', True, self.settings.white)
        self.settings.display.blit(count, (10,60))
        squished = self.settings.font_small.render(f'{str(self.settings.squished)} squished', True, self.settings.white)
        self.settings.display.blit(squished, (10,85))
        boost_left = self.settings.font.render('boost |', True, self.settings.black)
        self.settings.display.blit(boost_left, (int(self.settings.screen_width * 0.15), self.settings.screen_height * 0.85))
        left = self.settings.font.render('<', True, self.settings.black)
        self.settings.display.blit(left, (int(self.settings.screen_width * 0.40), self.settings.screen_height * 0.85))
        right = self.settings.font.render('>', True, self.settings.black)
        self.settings.display.blit(right, (int(self.settings.screen_width * 0.57), self.settings.screen_height * 0.85))
        boost_right = self.settings.font.render('| boost', True, self.settings.black)
        self.settings.display.blit(boost_right, (int(self.settings.screen_width * 0.70), self.settings.screen_height * 0.85))

    def squish_hitchhikers(self):
        for e in self.settings.enemies:
            squished = self.settings.pg.sprite.spritecollide(e, self.settings.hitchers, True, self.settings.pg.sprite.collide_mask)
            if squished:
                for h in squished:
                    h.play('squish')
                    h.kill()
                    self.settings.squished += 1

    def pick_up_hitchhikers(self):
        hitched = self.settings.pg.sprite.spritecollide(self.P1, self.settings.hitchers, True, self.settings.pg.sprite.collide_mask)
        if hitched:
            for h in hitched:
                h.play('ride')
                self.settings.rescued += 1

    def is_crash(self):
        return self.settings.pg.sprite.spritecollide(self.P1, self.settings.enemies, False, self.settings.pg.sprite.collide_mask)

    def handle_crash(self):
        self.settings.pg.mixer.Sound(self.settings.get_path('sounds', 'crash.wav')).play()
        pos = ( int(self.settings.screen_width / 2) - 150, int(self.settings.screen_height / 2) - 80)
        self.display_kill_and_fade(self.settings.red, self.settings.game_over, pos)

    def squished(self):
        return self.settings.squished >= self.settings.squish

    def handle_squished(self):
        got_squished = self.settings.font_medium.render(f"{self.settings.squished} hitchhiker{'' if self.settings.squished == 1 else 's'} got squished :(", True, self.settings.black)
        pos = ( int(self.settings.screen_width / 2) - 200, int(self.settings.screen_height / 2) - 80)
        self.display_kill_and_fade(self.settings.red, got_squished, pos)

    def level_up(self):
        return self.settings.rescued >= self.settings.rescue

    def handle_level_up(self):
        pos = ( int(self.settings.screen_width / 2) - 150, int(self.settings.screen_height / 2) - 80)
        self.display_kill_and_fade(self.settings.green, self.settings.level_up, pos)

    def display_kill_and_fade(self, color: tuple, surface, pos: tuple):
        time.sleep(0.5)
        self.settings.display.fill(color)
        self.settings.display.blit(surface, pos)
        self.settings.pg.display.update()
        for entity in self.settings.all_sprites:
            entity.kill()
        self.traffic.fadeout(2500)
        time.sleep(3)

