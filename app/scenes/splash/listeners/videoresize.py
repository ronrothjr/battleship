import pygame


class VideoResize:
    
    def add(self):
        return {pygame.VIDEORESIZE: self.on_video_resize}

    def on_video_resize(self, event: pygame.event.Event, game: pygame, scene):
        scene.set_bg(width=event.w, height=event.h)
