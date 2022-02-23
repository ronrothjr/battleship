import random, pygame
from settings import Settings
from utils import Utils


class Hitchhiker(pygame.sprite.Sprite):
    def __init__(self, settings: Settings):
        super().__init__()
        self.settings: Settings = settings
        self.id = random.choice([1,2,3,4,5,6])
        self.image = self.settings.pg.image.load(Utils.resource_path('tutorials', 'scroller', f"hitchhiker{self.id}.png"))
        self.rect = self.image.get_rect()
        self.mask = self.settings.pg.mask.from_surface(self.image)
        sides = []
        left = self.settings.margin + int(self.settings.left_shoulder_width / 2)
        sides.append(left)
        right = self.settings.margin + self.settings.left_shoulder_width + self.settings.lanes_width + int(self.settings.right_shoulder_width / 2)
        sides.append(right)
        side = random.choice(sides)
        if side == left:
            self.image = self.settings.pg.transform.flip(self.image, True, False)
        self.rect.center=(side, self.settings.screen_height * -0.05)
        
    def move(self):
        self.rect.move_ip(0, int(self.settings.speed / 2))
        if (self.rect.bottom > self.settings.screen_height + self.image.get_height()):
            self.kill()

    def play(self, reaction: str):
        self.settings.pg.mixer.Sound(Utils.resource_path('tutorials', 'scroller', f'{reaction}{self.id}.wav')).play()