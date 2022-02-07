import unittest
from unittest import mock
from unittest.mock import patch
from battleship_ui import BattleshipUI
from player import Player


class TestBattleshipUI(unittest.TestCase):

    def setUp(self) -> None:
        self.battleship_ui = BattleshipUI()

    def test_can_instantiate_a_battleship_ui(self):
        self.assertIsInstance(self.battleship_ui, BattleshipUI)
        self.assertEqual(self.battleship_ui.get_shot.__name__, 'get_shot') 
        self.assertTrue(callable(self.battleship_ui.get_shot))

    def test_ui_can_get_a_shot_from_a_player(self):
        fake_input = mock.Mock(side_effect=['E','5'])
        with patch('builtins.input', fake_input):
            coordinates = self.battleship_ui.get_shot(Player())
            self.assertEqual(coordinates, {'x': 'E', 'y': 5})


if __name__ == '__main__':
    unittest.main()
