import io, unittest
from unittest import mock
from unittest.mock import patch
from pynput.keyboard import Key
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
        self.session = Session(UI())

    @patch('sys.stdout', new_callable=io.StringIO)
    def add_players(self, mock_stdout):
        player_ship = Ship("Destroyer").set_location([Coordinates({'x': 'E', 'y': '5'}), Coordinates({'x': 'E', 'y': '6'})])
        player_grid = Grid().set_ships([player_ship])
        player = Player(player_grid)
        self.session.ui.enter_text('Bob')
        self.session.add_a_player(player)
        ai_ship = Ship("Destroyer").set_location([Coordinates({'x': 'B', 'y': '2'}), Coordinates({'x': 'B', 'y': '3'})])
        ai_grid = Grid().set_ships([ai_ship])
        ai = Player(ai_grid, 'AI', is_ai=True)
        self.session.add_a_player(ai)

    def test_can_instantiate_a_session(self):
        self.assertIsInstance(self.session, Session)
        self.assertIsInstance(self.session.watch, bool)
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

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_can_add_a_player(self):
        self.add_players()
        self.assertEqual(len(self.session.players), 2)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_can_place_ships_and__warn_player_of_rule_violation_ship_would_overlap(self, mock_stdout):
        player = Player()
        self.session.ui.sequence([Key.enter]) # E5 h
        self.session.ui.sequence([Key.space, Key.right, Key.up, Key.enter]) # D6 v
        self.session.ui.sequence([Key.space, Key.up, Key.up, Key.up, Key.left, Key.left, Key.left, Key.left, Key.enter]) # A2 v
        self.session.ui.sequence([Key.down, Key.down, Key.down, Key.down, Key.down, Key.down, Key.down, Key.down, Key.down, Key.right, Key.right, Key.enter]) # H4 h
        self.session.ui.sequence([Key.space, Key.up, Key.up, Key.up, Key.up, Key.up, Key.up, Key.up, Key.up, Key.right, Key.right, Key.right, Key.right, Key.right, Key.right, Key.enter]) # B0 v
        self.session.ui.sequence([Key.up, Key.left, Key.left, Key.left, Key.left, Key.left, Key.left, Key.enter]) # A4 h
        player = self.session.place_ships(player)
        output = mock_stdout.getvalue()
        self.assertIn("Bob broke a rule: Ship would overlap other ships", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_can_place_ships_and__warn_player_of_rule_violation_ship_would_extend_beyond(self, mock_stdout):
        player = Player()
        self.session.ui.sequence([Key.enter]) # E5 h
        self.session.ui.sequence([Key.space, Key.up, Key.up, Key.up, Key.left, Key.left, Key.left, Key.left, Key.enter]) # A2 v
        self.session.ui.sequence([Key.down, Key.down, Key.down, Key.down, Key.down, Key.down, Key.down, Key.down, Key.down, Key.right, Key.right, Key.enter]) # H4 h
        self.session.ui.sequence([Key.space, Key.up, Key.up, Key.up, Key.up, Key.up, Key.up, Key.up, Key.up, Key.right, Key.right, Key.right, Key.right, Key.right, Key.right, Key.enter]) # B0 v
        self.session.ui.sequence([Key.up, Key.left, Key.enter]) # A7 h
        self.session.ui.sequence([Key.left, Key.left, Key.left, Key.left, Key.left, Key.enter]) # A4 h
        self.session.place_ships(player)
        output = mock_stdout.getvalue()
        self.assertIn("Bob broke a rule: Ship would extend beyond grid", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_can_place_ships_for_player(self, mock_stdout):
        s5 = Ship("Carrier").set_location([
            Coordinates({'x': 'A', 'y': '4'}),
            Coordinates({'x': 'A', 'y': '5'}),
            Coordinates({'x': 'A', 'y': '6'}),
            Coordinates({'x': 'A', 'y': '7'}),
            Coordinates({'x': 'A', 'y': '8'})
        ])
        player = Player()
        self.session.ui.sequence([Key.enter]) # E5 h
        self.session.ui.sequence([Key.space, Key.up, Key.up, Key.up, Key.left, Key.left, Key.left, Key.left, Key.enter]) # A2 v
        self.session.ui.sequence([Key.down, Key.down, Key.down, Key.down, Key.down, Key.down, Key.down, Key.down, Key.down, Key.right, Key.right, Key.enter]) # H4 h
        self.session.ui.sequence([Key.space, Key.up, Key.up, Key.up, Key.up, Key.up, Key.up, Key.up, Key.up, Key.right, Key.right, Key.right, Key.right, Key.right, Key.right, Key.enter]) # B0 v
        self.session.ui.sequence([Key.up, Key.left, Key.left, Key.left, Key.left, Key.left, Key.enter]) # A4 h
        player = self.session.place_ships(player)
        self.assertEqual(player.grid.ships[4], s5)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_can_place_ships_for_ai(self, mock_stdout):
        player = Player(is_ai=True)
        self.session.place_ships(player)
        self.assertEqual(len(player.grid.ships), 5)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_players_can_take_a_turn(self, mock_stdout):
        self.add_players()
        self.session.ui.sequence([Key.enter]) # E5 h
        self.session.ui.sequence([Key.enter]) # E5 h
        self.session.ui.sequence([Key.down, Key.enter]) # F5 h
        turn = self.session.take_a_turn(self.session.players[0], self.session.players[1])
        self.assertTrue(turn in self.session.turns)
        self.assertEqual(turn.shot, Shot(Coordinates({'x': 'E', 'y': '5'})))
        turn = self.session.take_a_turn(self.session.players[0], self.session.players[1])
        self.assertTrue(turn in self.session.turns)
        self.assertEqual(turn.shot, Shot(Coordinates({'x': 'F', 'y': '5'})))

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_session_can_play_a_round(self, mock_stdout):
        self.add_players()
        self.session.ui.sequence([Key.up, Key.up, Key.up, Key.left, Key.left, Key.left, Key.enter])
        self.session.ui.sequence([Key.down, Key.down, Key.down, Key.right, Key.right, Key.right, Key.enter
        ])
        self.session.play_a_round()
        self.assertEqual(len(self.session.turns), 2)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_session_can_start_battle_until_all_oppenent_ships_are_destroyed(self, mock_stdout):
        self.add_players()
        self.session.ui.sequence([Key.left, Key.left, Key.left, Key.up, Key.up, Key.up, Key.enter]) # B2
        self.session.ui.sequence([Key.right, Key.enter]) # B3
        self.session.battle_until_one_is_defeated()
        self.session.display_game_result()
        self.assertEqual(len(self.session.turns), 3)
        output = mock_stdout.getvalue()
        self.assertIn('Bob is victorious!', output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_session_can_play_an_ai_game_by_itself(self, mock_stdout):
        self.session.play_a_game(ai_v_ai=True)
        output = mock_stdout.getvalue()
        self.assertIn('AI is victorious!', output)


if __name__ == '__main__':
    unittest.main()
