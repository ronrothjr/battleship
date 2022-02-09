import unittest
from session import Session
from game import Game
from data import Data
from files_mock import FilesMock


class TestGame(unittest.TestCase):

    def setUp(self) -> None:
        data_store = Data(FilesMock())
        self.game = Game(data_store=data_store)

    def test_can_instantiate_a_session(self):
        self.assertIsInstance(self.game, Game)
        self.assertIsInstance(self.game.data_store, Data)
        self.assertEqual(self.game.encode_game.__name__, 'encode_game') 
        self.assertTrue(callable(self.game.encode_game))
        self.assertEqual(self.game.save_a_game.__name__, 'save_a_game') 
        self.assertTrue(callable(self.game.save_a_game))
        self.assertEqual(self.game.load_a_game.__name__, 'load_a_game') 
        self.assertTrue(callable(self.game.load_a_game))

    def test_can_encode_game_to_save(self):
        session = Session()
        encoded_game = self.game.encode_game(session)
        self.assertEqual(encoded_game, {"watch": False, "ai": {}, "ui": {"spacing": 10, "grid_width": 45, "orientation": "landscape"}, "players": [], "turns": []})

    def test_can_save_a_game(self):
        session = Session()
        game_saved = self.game.save_a_game(session)
        self.assertTrue(game_saved)
        games = self.game.data_store.files.files['games.txt']
        self.assertIn('[{"watch": false, "ai": {}, "ui": {"spacing": 10, "grid_width": 45, "orientation": "landscape"}, "players": [], "turns": []', games)

    def test_can_load_a_game(self):
        game_str = '[{"watch": false, "ai": {}, "ui": {"spacing": 10, "grid_width": 45, "orientation": "landscape"}, "players": [], "turns": []}]'
        self.game.data_store.files.files['games.txt'] = game_str
        games = self.game.load_a_game()
        self.assertEqual(games, [{"watch": False, "ai": {}, "ui": {"spacing": 10, "grid_width": 45, "orientation": "landscape"}, "players": [], "turns": []}])


if __name__ == '__main__':
    unittest.main()
