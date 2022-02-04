import unittest
from battleship import Battleship


class TestBattleship(unittest.TestCase):
    def test_can_instantiate_a_shot(self):
        self.battleship = Battleship()
        self.assertIsInstance(self.battleship, Battleship)
        self.assertIsInstance(self.battleship.players, list)
        self.assertEqual(self.battleship.add_player.__name__, 'add_player') 
        self.assertTrue(callable(self.battleship.add_player))


if __name__ == '__main__':
    unittest.main()
