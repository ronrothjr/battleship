import unittest
from battleship_ai import BattleshipAI
from player import Player


class TestAI(unittest.TestCase):

    def setUp(self) -> None:
        self.ai = BattleshipAI()

    def test_can_instantiate_an_ai(self):
        self.assertIsInstance(self.ai, BattleshipAI)
        self.assertEqual(self.ai.get_shot.__name__, 'get_shot') 
        self.assertTrue(callable(self.ai.get_shot))

    def test_ai_can_return_a_random_set_of_x_y_coordinates_excluding_previous_shots(self):
        x_y = self.ai.get_shot(Player())
        self.assertIsInstance(x_y, dict)
        self.assertIsInstance(x_y['x'], str)
        self.assertIsInstance(x_y['y'], int)


if __name__ == '__main__':
    unittest.main()
