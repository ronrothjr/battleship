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
            return True
