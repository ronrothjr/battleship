from coordinates import Coordinates


class Ship:

    @staticmethod
    def models():
        return {
            "Destroyer": 2,
            "Cruiser": 3,
            "Submarine": 3,
            "Battleship": 4,
            "Carrier": 5
        }

    def __init__(self, model: str=None, load: dict=None) -> None:
        if load:
            self.model = load['model']
            self.size = load['size']
            self.location = [Coordinates(load=c) for c in load['location']]
        else:
            self.model = model
            self.size = (Ship.models())[model]
            self.location = []

    def set_location(self, location: list[Coordinates]) -> bool:
        if len(location) == self.size:
            self.location = location
            for coordinates in self.location:
                coordinates.model = self.model
            return self

    def is_sunk(self):
        is_damaged = [x for x in self.location if x.hit]
        is_sunk = len(is_damaged) == len(self.location)
        return is_sunk
