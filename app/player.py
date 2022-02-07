from coordinates import Coordinates
from grid import Grid
from ship import Ship
from shot import Shot


class Player:

    def __init__(self, grid: Grid=None, name: str='Bob', is_ai: bool=False) -> None:
        self.grid = grid if grid else Grid()
        self.name = name
        self.is_ai = is_ai

    def take_a_shot(self, shot: Shot=None):
        marked = self.grid.mark_shot(shot)
        if marked:
            return shot

    def is_defeated(self):
        is_ship_sunk = list(filter(lambda ship: ship.is_sunk(), self.grid.ships))
        is_defeated = len(is_ship_sunk) == len(self.grid.ships)
        return is_defeated

    