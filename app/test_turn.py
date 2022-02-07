import unittest
from coordinates import Coordinates
from grid import Grid
from player import Player
from shot import Shot
from turn import Turn


class TestTurn(unittest.TestCase):
    def test_can_instantiate_a_turn(self):
        grid = Grid()
        player = Player(grid)
        coordinates = Coordinates({'x': 'E', 'y': 5})
        shot = Shot(coordinates)
        self.turn = Turn(player, shot)
        self.assertIsInstance(self.turn, Turn)
        self.assertIsInstance(self.turn.player, Player)
        self.assertIsInstance(self.turn.shot, Shot)


if __name__ == '__main__':
    unittest.main()
