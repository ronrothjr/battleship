import pygame


class KeyDown:
    
    @staticmethod
    def add():
        return [{pygame.KEYDOWN: KeyDown.on_key_down}]

    @staticmethod
    def on_key_down(event: pygame.event.Event, game: pygame):
        if event.key == game.K_ESCAPE:
            game.event.post(game.event.Event(game.QUIT))
