import imp, inspect, os, pygame
from ctypes import Union
from inspect import signature


class EventPublisher:
    subscribers = {}

    def __init__(self, listeners=[]):
        self.__dict__ = self.subscribers
        self.listeners = []
        self.add_listeners(listeners)

    def __hash__(self):
        return 1

    def __eq__(self, other):
        try:
            return self.__dict__ is other.__dict__
        except:
            return 0

    def validate_listener(self, event_type: int, handler):
            if not isinstance(event_type, int):
                raise TypeError(f'event_type "{event_type}" must be an integer')
            if not callable(handler):
                raise TypeError('handler must be callable')
            sig = signature(handler)
            if not 'event' in sig.parameters:
                raise TypeError('handler must have a parameter named "event"')
            if not 'game' in sig.parameters:
                raise TypeError('handler must have a parameter named "game"')

    def add_listener(self, listener: dict):
        if not isinstance(listener, dict):
            raise TypeError('listener must be a dict')
        for event_type, handler in listener.items():
            self.validate_listener(event_type, handler)
            handlers = self.subscribers.get(event_type, [])
            handlers.append(handler)
            self.subscribers[event_type] = handlers

    def add_listeners(self, listeners: list[dict]):
        if not isinstance(listeners, list):
            raise TypeError('listeners must be a list of dict')
        for listener in listeners:
            self.add_listener(listener)

    def on_event(self, event: pygame.event.Event, game: pygame):
        if event.type in self.subscribers.keys():
            for handler in self.subscribers[event.type]:
                handler(event=event, game=game)

    def on_load(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(dir_path, 'listeners')
        for name in [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]:
            found_module = imp.find_module(name[:-3], [path])
            module = imp.load_module(name, *found_module)
            for obj in [obj for mem_name, obj in inspect.getmembers(module)]:
                if inspect.isclass(obj):
                    self.add_listeners(obj.add())
            found_module[0].close()
        return self
