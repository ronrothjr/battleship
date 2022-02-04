from grid import Grid


class Player:

    def __init__(self, grid: Grid=None, name: str='Bob', is_ai: bool=False) -> None:
        self.grid = grid if grid else Grid()
        self.name = name
        self.is_ai = is_ai