import random, pygame
from settings import Settings


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