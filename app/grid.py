from functools import reduce
from multiprocessing.dummy import current_process
from ship import Ship
from shot import Shot


class Grid:

    def __init__(self):
        self.shots: list[Shot] = []
        self.ships: list[Ship] = []

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

    def mark_shot(self, shot: Shot):
        shots_taken = self.get_all_shots_taken()
        already_taken = shot.coordinates in shots_taken
        if not already_taken:
            self.shots.append(shot)
            occupied = self.get_all_ship_coordinates()
            hits = list(filter(lambda c: c == shot.coordinates, occupied))
            shot.hit = len(hits) > 0
            return True
