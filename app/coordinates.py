class Coordinates:
    x: str
    y: int

    def __init__(self, location: dict):
        self.x = location['x']
        self.y = location['y']
        self.hit = False

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y