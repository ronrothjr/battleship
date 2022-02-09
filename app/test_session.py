import io, unittest
from unittest import mock
from unittest.mock import patch
from session import Session
from ai import AI
from game import Game
from ui import UI
from coordinates import Coordinates
from grid import Grid
from player import Player
from ship import Ship
from shot import Shot
from turn import Turn


class TestSession(unittest.TestCase):

    def setUp(self) -> None:
        self.session = Session()

    @patch('sys.stdout', new_callable=io.StringIO)
    def add_players(self, mock_stdout):
        player_ship = Ship("Destroyer").set_location([Coordinates({'x': 'E', 'y': '5'}), Coordinates({'x': 'E', 'y': '6'})])
        player_grid = Grid().set_ships([player_ship])
        player = Player(player_grid)
        fake_input = mock.Mock(side_effect=['Bob'])
        with patch('builtins.input', fake_input):
            self.session.add_a_player(player)
        ai_ship = Ship("Destroyer").set_location([Coordinates({'x': 'B', 'y': '2'}), Coordinates({'x': 'B', 'y': '3'})])
        ai_grid = Grid().set_ships([ai_ship])
        ai = Player(ai_grid, 'AI', is_ai=True)
        self.session.add_a_player(ai)

    def test_can_instantiate_a_session(self):
        self.assertIsInstance(self.session, Session)
        self.assertIsInstance(self.session.watch, bool)
        self.assertIsInstance(self.session.data, Game)
        self.assertIsInstance(self.session.ui, UI)
        self.assertIsInstance(self.session.ai, AI)
        self.assertIsInstance(self.session.players, list)
        self.assertIsInstance(self.session.turns, list)
        self.assertEqual(self.session.play_a_game.__name__, 'play_a_game') 
        self.assertTrue(callable(self.session.play_a_game))
        self.assertEqual(self.session.load_a_saved_game.__name__, 'load_a_saved_game') 
        self.assertTrue(callable(self.session.load_a_saved_game))
        self.assertEqual(self.session.play_a_loaded_game.__name__, 'play_a_loaded_game') 
        self.assertTrue(callable(self.session.play_a_loaded_game))
        self.assertEqual(self.session.add_a_player.__name__, 'add_a_player') 
        self.assertTrue(callable(self.session.add_a_player))
        self.assertEqual(self.session.place_ships.__name__, 'place_ships') 
        self.assertTrue(callable(self.session.place_ships))
        self.assertEqual(self.session.battle_until_one_is_defeated.__name__, 'battle_until_one_is_defeated') 
        self.assertTrue(callable(self.session.battle_until_one_is_defeated))
        self.assertEqual(self.session.display_game_result.__name__, 'display_game_result') 
        self.assertTrue(callable(self.session.display_game_result))
        self.assertEqual(self.session.play_a_round.__name__, 'play_a_round') 
        self.assertTrue(callable(self.session.play_a_round))
        self.assertEqual(self.session.take_a_turn.__name__, 'take_a_turn') 
        self.assertTrue(callable(self.session.take_a_turn))

    def test_can_add_a_player(self):
        self.add_players()
        self.assertEqual(len(self.session.players), 2)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_can_place_ships_and__warn_player_of_rule_violations(self, mock_stdout):
        fake_input = mock.Mock(side_effect=['E5', 'h', 'D6', 'v', 'A2', 'v', 'H4', 'h', 'B0', 'v', 'D5', 'h'])
        with patch('builtins.input', fake_input):
            player = Player()
            self.session.place_ships(player)
            output = mock_stdout.getvalue()
            self.assertIn("Bob broke a rule: Ship would overlap other ships\n", output)
        mock_stdout.truncate(0)
        mock_stdout.seek(0)
        fake_input = mock.Mock(side_effect=['E5', 'h', 'D9', 'h', 'A2', 'v', 'H4', 'h', 'B0', 'v', 'D5', 'h'])
        with patch('builtins.input', fake_input):
            player = Player()
            self.session.place_ships(player)
            output = mock_stdout.getvalue()
            self.assertIn("Bob broke a rule: Ship would extend beyond grid\n", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_can_place_ships_for_player(self, mock_stdout):
        s5 = Ship("Carrier").set_location([
            Coordinates({'x': 'D', 'y': '5'}),
            Coordinates({'x': 'D', 'y': '6'}),
            Coordinates({'x': 'D', 'y': '7'}),
            Coordinates({'x': 'D', 'y': '8'}),
            Coordinates({'x': 'D', 'y': '9'})
        ])
        fake_input = mock.Mock(side_effect=['E5', 'h', 'A2', 'v', 'H4', 'h', 'B0', 'v', 'D5', 'h'])
        with patch('builtins.input', fake_input):
            player = Player()
            self.session.place_ships(player)
            self.assertEqual(player.grid.ships[4].location, s5.location)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_can_place_ships_for_ai(self, mock_stdout):
        player = Player(is_ai=True)
        self.session.place_ships(player)
        self.assertEqual(len(player.grid.ships), 5)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_players_can_take_a_turn(self, mock_stdout):
        self.add_players()
        fake_input = mock.Mock(side_effect=['E5', 'E5', 'F5'])
        with patch('builtins.input', fake_input):
            turn = self.session.take_a_turn(self.session.players[0], self.session.players[1])
            self.assertTrue(turn in self.session.turns)
            self.assertTrue(turn.shot, Shot(Coordinates({'x': 'E', 'y': '5'})))
            turn = self.session.take_a_turn(self.session.players[0], self.session.players[1])
            self.assertTrue(turn in self.session.turns)
            self.assertTrue(turn.shot, Shot(Coordinates({'x': 'F', 'y': '5'})))

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_session_can_play_a_round(self, mock_stdout):
        self.add_players()
        fake_input = mock.Mock(side_effect=['B2', 'E5'])
        with patch('builtins.input', fake_input):
            self.session.play_a_round()
            self.assertEqual(len(self.session.turns), 2)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_session_can_start_battle_until_all_oppenent_ships_are_destroyed(self, mock_stdout):
        self.add_players()
        fake_input = mock.Mock(side_effect=['B2', 'C2', 'B3'])
        with patch('builtins.input', fake_input):
            self.session.battle_until_one_is_defeated()
            self.session.display_game_result()
            self.assertEqual(len(self.session.turns), 5)
            output = mock_stdout.getvalue()
            self.assertIn('Bob is victorious!\n', output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_session_can_play_an_ai_game_by_itself(self, mock_stdout):
        self.session.play_a_game(ai_v_ai=True)
        output = mock_stdout.getvalue()
        self.assertIn('AI is victorious!\n', output)


if __name__ == '__main__':
    unittest.main()
