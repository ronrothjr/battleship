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

    def __init__(self, model: str) -> None:
        self.model = model
        self.size = (Ship.models())[model]
        self.location = []

    def set_location(self, location: list[Coordinates]) -> bool:
        if len(location) == self.size:
            self.location = location
            return self

    def is_sunk(self):
        is_damaged = list(filter(lambda coordinates: coordinates.hit, self.location))
        is_sunk = len(is_damaged) == len(self.location)
        return is_sunk
