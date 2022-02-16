import datetime
from data import Data
from files import Files


class Storage:

    def __init__(self, data_store: Data=None) -> None:
        self.data_store = data_store if data_store else Data(Files())

    def encode_game(self, game_data):
        game = Data.get_object_dict(object_to_dict=game_data)
        return game

    def save_a_game(self, game_data):
        game = self.encode_game(game_data)
        games = self.data_store.load_records('games')
        timestamp = game.get('timestamp', datetime.datetime.today().strftime("%Y%m%d%H%M%S"))
        games[timestamp] = game
        self.data_store.save_records('games', games)
        return True

    def load_a_game(self):
        games = self.data_store.load_records('games')
        return games
