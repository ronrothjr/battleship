from operator import ne
import random
from coordinates import Coordinates
from grid import Grid
from player import Player
from shot import Shot


class AI:

    def __init__(self) -> None:
        pass

    def get_grid(self, x_y_taken=[]):
        grid = []
        [[grid.append({'x': x, 'y': y}) for x in Grid.x if {'x': x, 'y': y} not in x_y_taken] for y in Grid.y]
        return grid

    def place_ship(self, model: str, player: Player):
        x_y = random.choice(self.get_grid())
        orientation = random.choice(['h', 'v'])
        return x_y, orientation

    def get_shot(self, player: Player):
        shot = None
        all_shots_taken = player.grid.get_all_shots_taken()
        damaged_ship_coordinates = self.get_location_of_damaged_ship(player, all_shots_taken)
        if damaged_ship_coordinates:
            coordinates = self.get_shot_near_damaged_ship(all_shots_taken, damaged_ship_coordinates)
            if coordinates:
                shot = {'x': coordinates.x, 'y': coordinates.y}
        if shot is None:
            shot = self.get_random_shot(all_shots_taken)
        return shot

    def get_location_of_damaged_ship(self, player: Player, all_shots_taken: list[Coordinates]):
        damaged_ship_coordinates = []
        for coordinates in all_shots_taken:
            if coordinates.hit and not player.is_sunk(coordinates.model):
                damaged_ship_coordinates.append(coordinates)
        return damaged_ship_coordinates

    def get_shot_near_damaged_ship(self, all_shots_taken: list[Coordinates], damaged_ship_coordinates: list[Coordinates]):
        coordinates_near_damaged_ship = []
        for coordinates in damaged_ship_coordinates:
            coordinates_near_damaged_ship += self.add_nearby_coordinates(coordinates, all_shots_taken)
        if coordinates_near_damaged_ship:
            shot = random.choice(coordinates_near_damaged_ship)
            return shot

    def add_nearby_coordinates(self, coordinates: Coordinates, all_shots_taken: list[Coordinates]):
        nearby_coordinates = []
        x_index = Grid.x.index(coordinates.x)
        y_index = Grid.y.index(coordinates.y)
        left = Coordinates({'x': Grid.x[x_index - 1], 'y': coordinates.y}) if x_index > 0 else None
        up = Coordinates({'x': coordinates.x, 'y': Grid.y[y_index - 1]}) if y_index > 0 else None
        right = Coordinates({'x': Grid.x[x_index + 1], 'y': coordinates.y}) if x_index < 9 else None
        down = Coordinates({'x': coordinates.x, 'y': Grid.y[y_index + 1]}) if y_index < 9 else None
        is_unused = lambda c: not c in all_shots_taken and not c in nearby_coordinates
        if left and is_unused(left):
            nearby_coordinates.append(left)
        if up and is_unused(up):
            nearby_coordinates.append(up)
        if right and is_unused(right):
            nearby_coordinates.append(right)
        if down and is_unused(down):
            nearby_coordinates.append(down)
        return nearby_coordinates

    def get_random_shot(self, all_shots_taken: list[Coordinates]):
        x_y_taken = [{'x': c.x, 'y': c.y} for c in all_shots_taken]
        shots_available = self.get_grid(x_y_taken)
        shot = random.choice(shots_available)
        return shot
