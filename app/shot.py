from coordinates import Coordinates


class Shot:

    def __init__(self, coordinates: Coordinates=None, hit: bool=False, load: dict=None) -> None:
        if load:
            self.coordinates = Coordinates(load=load['coordinates'])
            self.hit = load['hit']
            self.model = load['model']
        else:
            self.coordinates = coordinates
            self.hit = hit
            self.model = ''

    def __eq__(self, other):
        return self.coordinates.x == other.coordinates.x and self.coordinates.y == other.coordinates.y
