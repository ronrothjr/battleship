import unittest
from unittest.mock import patch
from game import Game


class TestGame(unittest.TestCase):
    
    def setUp(self):
        self.game = Game()

    def test_can_instantiate_game(self):
        self.assertIsInstance(self.game, Game)
        self.assertTrue(callable(self.game.on_execute))

    @patch.object(Game, 'on_init')
    def test_can_execute_the_game(self, mock_on_init):
        self.game.on_execute()
        self.assertTrue(mock_on_init.called)


if __name__ == '__main__':
    unittest.main()
