from coordinates import Coordinates


class Shot:

    def __init__(self, coordinates: Coordinates, hit: bool=False) -> None:
        self.coordinates = coordinates
        self.hit = hit
        self.model = ''