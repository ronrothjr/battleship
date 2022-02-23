import pygame, os, copy
from settings import Settings

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


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
        up = self.rect.topleft[1] > self.settings.SCREEN_HEIGHT * 0.55 and (move == 'boost' or pressed_keys[self.settings.pg.K_UP] or pressed_keys[self.settings.pg.K_w])
        not_bottom = self.rect.bottomright[1] < self.settings.SCREEN_HEIGHT * 0.8 + int( self.rect.height / 2 )
        down = not_bottom and (pressed_keys[self.settings.pg.K_SPACE])
        left = self.rect.left > self.settings.MARGIN + self.settings.LEFT_SHOULDER and (move == 'left' or pressed_keys[self.settings.pg.K_LEFT] or pressed_keys[self.settings.pg.K_a])
        right = self.rect.right < self.settings.SCREEN_WIDTH - self.settings.RIGHT_SHOULDER and (move == 'right' or pressed_keys[self.settings.pg.K_RIGHT] or pressed_keys[self.settings.pg.K_d])
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
