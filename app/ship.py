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
            self.sunk = load['sunk']
        else:
            self.model = model
            self.size = (Ship.models())[model]
            self.location = []
            self.sunk = False

    def set_location(self, location: list[Coordinates]) -> bool:
        if len(location) == self.size:
            self.location = location
            for coordinates in self.location:
                coordinates.model = self.model
            return self

    def is_sunk(self):
        if self.sunk:
            return self.sunk
        is_damaged = []
        for x in self.location:
            if x.hit == True:
                is_damaged.append(x)
        is_sunk = is_damaged == self.location
        self.sunk = is_sunk
        if is_damaged:
            is_sunk
        return is_sunk
