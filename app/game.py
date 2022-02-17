import pygame
from event_publisher import EventPublisher
import asset_utils

class Game():

    def __init__(self, pg: pygame):
        self.pg = pg
        self._running = True
        self.screen = None
        self.surface = None
        self.size = self.width, self.height = 756, 755
        self.publisher = EventPublisher([{self.pg.QUIT: self.on_exit}]).on_load()
        self.on_init()

    def on_init(self) -> bool:
        self.pg.init()
        self._running = True

    def start(self):
        self.on_start()
        self.event_loop()
        self.on_cleanup()

    def event_loop(self):
        while self._running:
            events = self.pg.event.get()
            for event in events:
                self.publisher.on_event(event=event, game=self.pg)
            self.on_loop()
            self.on_render()

    def on_start(self):
        self.screen = self.pg.display.set_mode(self.size, self.pg.NOFRAME, self.pg.FULLSCREEN)
        image_path = asset_utils.resource_path('assets', 'images', 'battleship.jpeg')
        self.surface = self.pg.image.load(image_path).convert()
        self.screen.blit(self.surface, (0,0))

    def on_exit(self, event: pygame.event.Event, game: pygame):
        self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        self.pg.display.flip()

    def on_cleanup(self):
        self.pg.quit()
