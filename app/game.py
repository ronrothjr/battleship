import pygame
from pygame.locals import *
from event_publisher import EventPublisher
import asset_utils

class Game():

    def __init__(self, pygame: pygame):
        self.pygame = pygame
        self._running = True
        self.screen = None
        self.image = None
        self.size = self.width, self.height = 756, 755
        self.publisher = EventPublisher()
        self.on_init()

    def on_init(self) -> bool:
        self.pygame.init()
        self._running = True

    def start(self):
        self.on_start()
        self.event_loop()
        self.on_cleanup()

    def event_loop(self):
        while self._running:
            events = self.pygame.event.get()
            for event in events:
                self.publisher.on_event(event=event, game=self.pygame)
            self.on_loop()
            self.on_render()

    def on_start(self):
        self.screen = self.pygame.display.set_mode(self.size, NOFRAME, FULLSCREEN)
        image_path = asset_utils.resource_path('assets', 'images', 'battleship.jpeg')
        self.surface = self.pygame.image.load(image_path).convert()
        self.screen.blit(self.surface, (0,0))
        self.publisher.add_listeners([{QUIT: self.on_exit}, {KEYDOWN: self.on_key_down}])

    def on_exit(self, event: pygame.event.Event, game: pygame):
        self._running = False

    def on_key_down(self, event: pygame.event.Event, game: pygame):
        if event.key == K_ESCAPE:
            game.event.post(game.event.Event(QUIT))

    def on_loop(self):
        pass

    def on_render(self):
        self.pygame.display.flip()

    def on_cleanup(self):
        self.pygame.quit()
