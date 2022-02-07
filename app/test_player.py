import unittest
from coordinates import Coordinates
from grid import Grid
from player import Player
from ship import Ship
from shot import Shot


class TestPlayer(unittest.TestCase):

    def test_can_instantiate_a_shot(self):
        grid = Grid()
        player = Player(grid)
        self.assertIsInstance(player, Player)
        self.assertIsInstance(player.name, str)
        self.assertIsInstance(player.is_ai, bool)
        self.assertIsInstance(player.grid, Grid)
        self.assertEqual(player.take_a_shot.__name__, 'take_a_shot') 
        self.assertTrue(callable(player.take_a_shot))
        self.assertEqual(player.is_defeated.__name__, 'is_defeated') 
        self.assertTrue(callable(player.is_defeated))

    def test_player_can_take_a_shot_and_record_a_hit(self):
        grid = Grid()
        player = Player(grid)
        ship1 = Ship('Destroyer').set_location([Coordinates({'x': 'E', 'y': '5'}), Coordinates({'x': 'E', 'y': '6'})])
        player.grid.add_ship(ship1)
        shot = Shot(Coordinates({'x': 'E', 'y': '5'}))
        shot_taken = player.take_a_shot(shot)
        self.assertIsInstance(shot_taken, Shot)
        self.assertTrue(shot_taken.hit)

    def test_player_can_tell_if_is_defeated(self):
        grid = Grid()
        player = Player(grid)
        ship1 = Ship('Destroyer')
        ship1.set_location([Coordinates({'x': 'E', 'y': '5'}), Coordinates({'x': 'E', 'y': '6'})])
        player.grid.add_ship(ship1)
        shot = Shot(Coordinates({'x': 'E', 'y': '5'}))
        player.take_a_shot(shot)
        shot = Shot(Coordinates({'x': 'E', 'y': '6'}))
        player.take_a_shot(shot)
        is_defeated = player.is_defeated()
        self.assertTrue(is_defeated)



if __name__ == '__main__':
    unittest.main()
