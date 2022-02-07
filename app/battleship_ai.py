import random
from coordinates import Coordinates
from player import Player


class BattleshipAI:

    def __init__(self) -> None:
        self.x = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        self.y = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def get_shot(self, player: Player):
        all_shots_taken = player.grid.get_all_shots_taken()
        shot = self.get_random_shot(all_shots_taken)
        return shot

    def get_random_shot(self, all_shots_taken: list[Coordinates]):
        x_y_taken = [{'x': c.x, 'y': c.y} for c in all_shots_taken]
        shots_available = []
        [[shots_available.append({'x': x, 'y': y}) for x in self.x if {'x': x, 'y': y} not in x_y_taken] for y in self.y]
        shot = random.choice(shots_available)
        return shot
