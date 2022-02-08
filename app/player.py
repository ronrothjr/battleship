from coordinates import Coordinates
from grid import Grid
from ship import Ship
from shot import Shot


class Player:

    def __init__(self, grid: Grid=None, name: str='Bob', is_ai: bool=False) -> None:
        self.grid = grid if grid else Grid()
        self.name = 'AI' if is_ai else name
        self.is_ai = is_ai

    def take_a_shot(self, shot: Shot=None):
        marked = self.grid.mark_shot(shot)
        return shot

    def is_sunk(self, model: str):
        return self.grid.get_ship(model).is_sunk()

    def is_defeated(self):
        is_sunk = lambda ship: ship.is_sunk()
        is_ship_sunk = [x for x in self.grid.ships if is_sunk(x)]
        is_defeated = len(is_ship_sunk) == len(self.grid.ships)
        return is_defeated

    