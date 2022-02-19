import os, sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from event_publisher import EventPublisher
from director import Director


class Game():

    def __init__(self, pg: pygame):
        self.pg = pg
        self._running = False
        self.director = None
        self.publisher = None
        self.fps = None

    def on_init(self, settings: dict) -> 'Game':
        self.director = Director(self.pg, settings)
        self.publisher = EventPublisher({self.pg.QUIT: self.on_exit})
        self.fps = self.pg.time.Clock()
        self.pg.init()
        self._running = True
        return self

    def start(self) -> None:
        self.on_start()
        self.event_loop()
        self.on_cleanup()

    def on_start(self) -> None:
        self.director.call('splash')

    def event_loop(self) -> None:
        while self._running:
            events = self.pg.event.get()
            for event in events:
                self.publisher.on_event(event=event, game=self.pg, scene=self.director.current_scene)
            self.on_loop()
            self.on_render()
            self.fps.tick(60)

    def on_cleanup(self) -> None:
        self.pg.quit()
        sys.exit()

    def on_exit(self, event: pygame.event.Event, game: pygame, scene) -> None:
        self._running = False

    def on_loop(self) -> None:
        pass

    def on_render(self) -> None:
        self.pg.display.flip()
