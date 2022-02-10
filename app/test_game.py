import json, unittest
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
        self.assertEqual(list(encoded_game.keys()), ['timestamp', 'watch', 'players', 'turns'])

    def test_can_save_a_game(self):
        session = Session()
        timestamp = session.timestamp
        game_saved = self.game.save_a_game(session)
        self.assertTrue(game_saved)
        games = json.loads(self.game.data_store.files.files['games.txt'])
        game = games[timestamp]
        self.assertEqual(list(game.keys()), ['timestamp', 'watch', 'players', 'turns'])

    def test_can_load_a_game(self):
        session = Session()
        timestamp = session.timestamp
        game_str = '{"' + timestamp + '": {"timestamp": "' + timestamp + '", "watch": false, "players": [], "turns": []}}'
        self.game.data_store.files.files['games.txt'] = game_str
        games = self.game.load_a_game()
        game = games[timestamp]
        self.assertEqual(list(game.keys()), ['timestamp', 'watch', 'players', 'turns'])


if __name__ == '__main__':
    unittest.main()
