import sys, os
from pygame.locals import *
from event_publisher import EventPublisher


def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Game():

    def __init__(self, pygame):
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
        self.on_start()

    def start(self):
        while self._running:
            events = self.pygame.event.get()
            for event in events:
                self.publisher.on_event(event=event, game=self.pygame)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

    def on_start(self):
        self.screen = self.pygame.display.set_mode(self.size, NOFRAME, FULLSCREEN)
        self.image = self.pygame.image.load(resource_path(os.path.join('images', 'battleship.jpeg'))).convert()
        self.publisher.add_listener({QUIT: self.on_exit})
        self.publisher.add_listener({KEYDOWN: self.on_key_down})

    def on_exit(self, event, game):
        self._running = False

    def on_key_down(self, event, game):
        if event.key == K_ESCAPE:
            game.event.post(game.event.Event(QUIT))

    def on_loop(self):
        pass

    def on_render(self):
        self.screen.blit(self.image, (0,0))
        self.pygame.display.flip()

    def on_cleanup(self):
        self.pygame.quit()
