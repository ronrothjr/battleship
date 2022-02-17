import copy

class MockLoadedImage:
    def __init__(self, file_name):
        self.file_name = file_name

    def convert(self):
        pass

class MockImageSurface:
    pass

class MockDisplaySurface:
    def __init__(self, size):
        self.size = size

    def blit(self, image, location):
        pass

class MockDisplay:
    def set_mode(self, size, *args):
        self.size = size
        return MockDisplaySurface(size)

    def flip(self):
        pass

class MockImage:
    def load(self, file_name):
        return MockLoadedImage(file_name)

class Event:
    def __init__(self, type: int):
        self.type = type
    def __str__(self):
        return str(self.__dict__)

class MockEvent:
    queue = []
    Event = Event

    def get(self, event_filter=None):
        events = copy.deepcopy(self.queue)
        self.queue = []
        return events

    def post(self, event):
        self.queue.append(event)

class MockPygame:

    FULLSCREEN = 1
    NOFRAME = 2
    QUIT = 123
    KEYDOWN = 576
    K_ESCAPE = 27

    event = MockEvent()

    def init(self):
        self.display = MockDisplay()
        self.image = MockImage()
    
    def quit(self):
        pass
