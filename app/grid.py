from coordinates import Coordinates
from ship import Ship
from shot import Shot


class Grid:

    x = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    y = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

    @staticmethod
    def get_location_coordinates(model, x_y, orientation):
        coordinates = []
        size = Ship.models()[model]
        x_index = Grid.x.index(x_y['x'])
        y_index = Grid.y.index(x_y['y'])        
        for l in range(0, size):
            x_coordinate_index = x_index + (l if orientation == 'v' else 0)
            y_coordinate_index = y_index + (l if orientation == 'h' else 0)
            if x_coordinate_index > 9 or y_coordinate_index > 9:
                return
            x_y_dict = {'x': Grid.x[x_coordinate_index],'y': Grid.y[y_coordinate_index]}
            coordinates.append(Coordinates(x_y_dict))
        return coordinates

    def __init__(self):
        self.ships = []
        self.shots = []

    def set_ships(self, ships):
        self.ships = ships
        return self

    def set_shots(self, shots):
        self.shots = shots
        return self

    def get_all_ship_coordinates(self):
        occupied = []
        for ship in self.ships:
            occupied += ship.location
        return occupied

    def get_all_ship_models(self):
        models = []
        for ship in self.ships:
            models.append(ship.model)
        return models

    def get_all_shots_taken(self):
        shots_taken = []
        for shot in self.shots:
            shots_taken.append(shot.coordinates)
        return shots_taken

    def add_ship(self, ship: Ship):
        occupied = self.get_all_ship_coordinates()
        blocked = list(filter(lambda coord: coord in occupied, ship.location))
        current_models = self.get_all_ship_models()
        added = ship.model in current_models
        if not blocked and not added:
            self.ships.append(ship)
            return True

    def is_shot_already_taken(self, shot: Shot):
        shots_taken = self.get_all_shots_taken()
        already_taken = shot.coordinates in shots_taken
        return already_taken

    def mark_shot(self, shot: Shot):
        already_taken = self.is_shot_already_taken(shot)
        if not already_taken:
            self.shots.append(shot)
            occupied = self.get_all_ship_coordinates()
            self.record_hits(shot, occupied)
            return True
    
    def record_hits(self, shot: Shot, occupied: list[Coordinates]):
        for coordinates in occupied:
            if coordinates == shot.coordinates:
                coordinates.hit = True
                shot.hit = True
                shot.model = coordinates.model
