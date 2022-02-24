import pygame, os, copy
from settings import Settings
from utils import Utils

# abspath = os.path.abspath(__file__)
# dname = os.path.dirname(abspath)
# os.chdir(dname)


class Player(pygame.sprite.Sprite):
    def __init__(self, settings: Settings):
        super().__init__()
        self.settings: Settings = settings
        self.image = self.settings.pg.image.load(self.settings.get_path('images', "player.png"))
        self.image = self.settings.scale_image(self.image)
        self.width = self.image.get_width()
        self.half_width = int(self.width / 2)
        self.original_image = copy.copy(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (int(self.settings.screen_width / 2), int(self.settings.screen_height * 0.8))
        self.angle = 0
        self.boost = 0
        self.boosting = False
        self.recharge = 0
        self.left = self.rect.topleft[0]
        self.top = self.rect.topleft[1]
        self.mask = self.settings.pg.mask.from_surface(self.image)

    def move(self, move: str=''):
        speed = self.settings.scale(self.settings.speed)
        pressed_keys = self.settings.pg.key.get_pressed()
        pressed_left = move == 'left' or pressed_keys[self.settings.pg.K_LEFT] or pressed_keys[self.settings.pg.K_a]
        pressed_right = move == 'right' or pressed_keys[self.settings.pg.K_RIGHT] or pressed_keys[self.settings.pg.K_d]
        up = self.rect.topleft[1] > self.settings.screen_height * 0.55 and (move == 'boost' or pressed_keys[self.settings.pg.K_UP] or pressed_keys[self.settings.pg.K_w])
        not_bottom = self.rect.bottomright[1] < self.settings.screen_height * 0.8 + int( self.rect.height / 2 )
        down = not_bottom and (pressed_keys[self.settings.pg.K_SPACE])
        center = self.rect.centerx
        left = pressed_left and center > self.settings.left_edge
        right = pressed_right and center < self.settings.right_edge
        x_change = 0
        y_change = 0

        if up:
            if (self.recharge == 0 or self.boosting):
                if not self.boosting:
                    self.recharge = 180
                    self.boosting = True
                if self.boost < speed:
                    if self.boost == 0:
                        self.settings.pg.mixer.Sound(self.settings.get_path('sounds', 'boost.wav')).play()
                    self.boost += int(speed / 5)
                else:
                    self.boosting = False
            move = 'up'

        elif down:
            y_change = int(speed / 2)
            move = 'down'

        if left:
            if self.angle < self.settings.turn_radius:
                self.angle += int(speed / 5) * 2

        elif right:
            if self.angle > -self.settings.turn_radius:
                self.angle -= int(speed / 5) * 2

        if self.angle != 0:
            boost = self.settings.scale(self.boost)
            x_change = int((speed + boost) / 3 * (self.angle / self.settings.turn_radius * -1))
            self.set_rotation()

        if self.boost > 0:
            y_change -= self.boost
            if not up:
                self.boost -= int(speed / 5)
        elif not_bottom:
            y_change += int(speed / 5)

        if self.recharge > 0:
            self.recharge -= int(self.settings.speed / 5)

        is_too_far_left = self.left + x_change < self.settings.left_edge
        is_too_far_right = self.left + x_change + self.width > self.settings.right_edge
        if is_too_far_left:
            x_change = self.left - self.settings.left_edge
        if is_too_far_right:
            x_change = self.settings.right_edge - (self.left + self.width)
        self.rect.move_ip(x_change, y_change)
        self.left += x_change
        self.top += y_change
        if not up and not down and not left and not right:
            move = ''
            if self.angle != 0:
                self.angle += -int(speed / 5) * 2 if self.angle > 0 else int(speed / 5) * 2
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
