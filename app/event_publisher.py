import imp, inspect, os, pygame
from ctypes import Union
from inspect import signature


class EventPublisher:
    subscribers = {}

    def __init__(self, listeners={}):
        self.__dict__ = self.subscribers
        self.subscribe(listeners)

    def __hash__(self):
        return 1

    def __eq__(self, other):
        try:
            return self.__dict__ is other.__dict__
        except:
            return 0

    def validate_listener(self, event_type: int, func):
            if not isinstance(event_type, int):
                raise TypeError(f'event_type "{event_type}" must be an integer')
            if not callable(func):
                raise TypeError('handler must be callable')
            sig = signature(func)
            if not 'event' in sig.parameters:
                raise TypeError('handler must have a parameter named "event"')
            if not 'game' in sig.parameters:
                raise TypeError('handler must have a parameter named "game"')

    def subscribe(self, listeners: dict, scene: str='default'):
        if not isinstance(listeners, dict):
            raise TypeError('listener must be a dict')
        for event_type, func in listeners.items():
            self.validate_listener(event_type, func)
            handlers = self.subscribers.get(event_type, [])
            handlers.append({'scene': scene, 'func': func})
            self.subscribers[event_type] = handlers

    def on_event(self, event: pygame.event.Event, game: pygame):
        if event.type in self.subscribers.keys():
            for handler in self.subscribers[event.type]:
                handler.get('func')(event=event, game=game)

    def on_load(self, scene_name: str):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(dir_path, 'scenes', scene_name, 'listeners')
        for name in [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]:
            found_module = imp.find_module(name[:-3], [path])
            module = imp.load_module(name, *found_module)
            for obj in [obj for mem_name, obj in inspect.getmembers(module) if inspect.isclass(obj)]:
                self.subscribe(listeners=obj().add(), scene=scene_name)
            found_module[0].close()
        return self

    def on_unload(self, scene_name: str):
        updated_subscribers = {}
        for name, subscribers in self.subscribers.items():
            listeners = []
            for listener in subscribers:
                if not listener.get('scene') == scene_name:
                    listeners.append(listener)
            if listeners:
                updated_subscribers[name] = listeners
        self.subscribers = updated_subscribers
