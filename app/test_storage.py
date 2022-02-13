import json, unittest
from session import Session
from storage import Storage
from data import Data
from files_mock import FilesMock


class TestStorage(unittest.TestCase):

    def setUp(self) -> None:
        data_store = Data(FilesMock())
        self.storage = Storage(data_store=data_store)

    def test_can_instantiate_a_session(self):
        self.assertIsInstance(self.storage, Storage)
        self.assertIsInstance(self.storage.data_store, Data)
        self.assertEqual(self.storage.encode_game.__name__, 'encode_game') 
        self.assertTrue(callable(self.storage.encode_game))
        self.assertEqual(self.storage.save_a_game.__name__, 'save_a_game') 
        self.assertTrue(callable(self.storage.save_a_game))
        self.assertEqual(self.storage.load_a_game.__name__, 'load_a_game') 
        self.assertTrue(callable(self.storage.load_a_game))

    def test_can_encode_game_to_save(self):
        session = Session()
        encoded_game = self.storage.encode_game(session)
        self.assertEqual(list(encoded_game.keys()), ['timestamp', 'watch', 'players', 'turns'])

    def test_can_save_a_game(self):
        session = Session()
        timestamp = session.timestamp
        game_saved = self.storage.save_a_game(session)
        self.assertTrue(game_saved)
        games = json.loads(self.storage.data_store.files.files['games.txt'])
        game = games[timestamp]
        self.assertEqual(list(game.keys()), ['timestamp', 'watch', 'players', 'turns'])

    def test_can_load_a_game(self):
        session = Session()
        timestamp = session.timestamp
        game_str = '{"' + timestamp + '": {"timestamp": "' + timestamp + '", "watch": false, "players": [], "turns": []}}'
        self.storage.data_store.files.files['games.txt'] = game_str
        games = self.storage.load_a_game()
        game = games[timestamp]
        self.assertEqual(list(game.keys()), ['timestamp', 'watch', 'players', 'turns'])


if __name__ == '__main__':
    unittest.main()
