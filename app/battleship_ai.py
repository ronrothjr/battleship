import random
from coordinates import Coordinates
from grid import Grid
from player import Player
from ship import Ship


class BattleshipAI:

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
        all_shots_taken = player.grid.get_all_shots_taken()
        shot = self.get_random_shot(all_shots_taken)
        return shot

    def get_random_shot(self, all_shots_taken: list[Coordinates]):
        x_y_taken = [{'x': c.x, 'y': c.y} for c in all_shots_taken]
        shots_available = self.get_grid(x_y_taken)
        shot = random.choice(shots_available)
        return shot
