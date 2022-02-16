from inspect import signature


class EventPublisher:
    subscribers = {}

    def __init__(self): self.__dict__ = self.subscribers

    def __hash__(self): return 1

    def __eq__(self, other):
        try:
            return self.__dict__ is other.__dict__
        except:
            return 0

    def add_listener(self, listener: dict):
        if not isinstance(listener, dict):
            raise TypeError('listener must be a dict')
        for event_type, handler in listener.items():
            if not isinstance(event_type, int):
                raise TypeError(f'event_type "{event_type}" must be an integer')
            if not callable(handler):
                raise TypeError('handler must be callable')
            sig = signature(handler)
            if not 'event' in sig.parameters:
                raise TypeError('handler must have a parameter named "event"')
            if not 'game' in sig.parameters:
                raise TypeError('handler must have a parameter named "game"')
            handlers = self.subscribers.get(event_type, [])
            handlers.append(handler)
            self.subscribers[event_type] = handlers

    def on_event(self, event, game):
        print(event)
        if event.type in self.subscribers.keys():
            for handler in self.subscribers[event.type]:
                handler(event=event, game=game)
