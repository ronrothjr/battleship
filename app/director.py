import pygame
from event_publisher import EventPublisher
from setting import Setting


class Director:

    def __init__(self, pg: pygame, settings: dict={}):
        self.scenes = {}
        self.pg = pg
        self.set_scenes(settings)
        self.current_scene: Setting = None
        self.publisher = EventPublisher()

    def set_scenes(self, settings: dict):
        for name, setting in settings.items():
            self.scenes[name] = Setting(self.pg, name, setting)

    def call(self, scene_name):
        if self.current_scene:
            self.cut(self.current_scene.name)
        scene: Setting = self.scenes[scene_name]
        scene.on_init()
        self.current_scene = scene
        self.publisher.on_load(scene_name)

    def cut(self, scene_name):
        scene: Setting = self.scenes[scene_name]
        scene.on_exit()
        self.publisher.on_unload(scene_name)
        self.current_scene = None
