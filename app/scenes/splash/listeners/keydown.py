import pygame


class KeyDown:
    
    def add(self):
        return {pygame.KEYDOWN: self.on_key_down}

    def on_key_down(self, event: pygame.event.Event, game: pygame, scene):
        if event.key == game.K_ESCAPE:
            game.event.post(game.event.Event(game.QUIT))
