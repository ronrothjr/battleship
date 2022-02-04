import unittest
from grid import Grid
from player import Player


class TestShot(unittest.TestCase):
    def test_can_instantiate_a_shot(self):
        grid = Grid()
        self.player = Player(grid)
        self.assertIsInstance(self.player, Player)
        self.assertIsInstance(self.player.name, str)
        self.assertIsInstance(self.player.is_ai, bool)
        self.assertIsInstance(self.player.grid, Grid)


if __name__ == '__main__':
    unittest.main()
