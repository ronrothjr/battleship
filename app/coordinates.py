class Coordinates:
    x: str
    y: str
    hit: bool
    model: str

    def __init__(self, location: dict=None, load: dict=None):
        if load:
            self.x = load['x']
            self.y = load['y']
            self.hit = load['hit']
            self.model = load['model']
        else:
            self.x = location['x']
            self.y = location['y']
            self.hit = False
            self.model = ''

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y