import pygame


class MouseButtonDown:
    
    def add(self):
        return {pygame.MOUSEBUTTONDOWN: self.on_mouse_button_down}

    def on_mouse_button_down(self, event: pygame.event.Event, game: pygame, scene):
        game.event.post(game.event.Event(game.QUIT))
