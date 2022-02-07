import io, unittest
from unittest import mock
from unittest.mock import patch
from battleship import Battleship
from battleship_ai import BattleshipAI
from battleship_ui import BattleshipUI
from coordinates import Coordinates
from grid import Grid
from player import Player
from ship import Ship
from shot import Shot
from turn import Turn


class TestBattleship(unittest.TestCase):

    def setUp(self) -> None:
        self.battleship = Battleship()

    def add_players(self):
        player_ship = Ship("Destroyer").set_location([Coordinates({'x': 'E', 'y': '5'}), Coordinates({'x': 'E', 'y': '6'})])
        player_grid = Grid().set_ships([player_ship])
        player = Player(player_grid)
        fake_input = mock.Mock(side_effect=['Bob'])
        with patch('builtins.input', fake_input):
            self.battleship.add_a_player(player)
        ai_ship = Ship("Destroyer").set_location([Coordinates({'x': 'B', 'y': '2'}), Coordinates({'x': 'B', 'y': '3'})])
        ai_grid = Grid().set_ships([ai_ship])
        ai = Player(ai_grid, 'AI', is_ai=True)
        self.battleship.add_a_player(ai)

    def test_can_instantiate_a_battleship(self):
        self.assertIsInstance(self.battleship, Battleship)
        self.assertIsInstance(self.battleship.watch, bool)
        self.assertIsInstance(self.battleship.ui, BattleshipUI)
        self.assertIsInstance(self.battleship.ai, BattleshipAI)
        self.assertIsInstance(self.battleship.players, list)
        self.assertIsInstance(self.battleship.turns, list)
        self.assertEqual(self.battleship.play_a_game.__name__, 'play_a_game') 
        self.assertTrue(callable(self.battleship.play_a_game))
        self.assertEqual(self.battleship.add_a_player.__name__, 'add_a_player') 
        self.assertTrue(callable(self.battleship.add_a_player))
        self.assertEqual(self.battleship.place_ships.__name__, 'place_ships') 
        self.assertTrue(callable(self.battleship.place_ships))
        self.assertEqual(self.battleship.battle_until_one_is_defeated.__name__, 'battle_until_one_is_defeated') 
        self.assertTrue(callable(self.battleship.battle_until_one_is_defeated))
        self.assertEqual(self.battleship.play_a_round.__name__, 'play_a_round') 
        self.assertTrue(callable(self.battleship.play_a_round))
        self.assertEqual(self.battleship.take_a_turn.__name__, 'take_a_turn') 
        self.assertTrue(callable(self.battleship.take_a_turn))

    def test_can_add_a_player(self):
        self.add_players()
        self.assertEqual(len(self.battleship.players), 2)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_can_place_ships_and__warn_player_of_rule_violations(self, mock_stdout):
        fake_input = mock.Mock(side_effect=['E', '5', 'h', 'D', '6', 'v', 'A', '2', 'v', 'H', '4', 'h', 'B', '0', 'v', 'D', '5', 'h'])
        with patch('builtins.input', fake_input):
            player = Player()
            self.battleship.place_ships(player)
            output = mock_stdout.getvalue()
            self.assertIn("Bob broke a rule: Ship would overlap other ships\n", output)
        mock_stdout.truncate(0)
        mock_stdout.seek(0)
        fake_input = mock.Mock(side_effect=['E', '5', 'h', 'D', '9', 'h', 'A', '2', 'v', 'H', '4', 'h', 'B', '0', 'v', 'D', '5', 'h'])
        with patch('builtins.input', fake_input):
            player = Player()
            self.battleship.place_ships(player)
            output = mock_stdout.getvalue()
            self.assertIn("Bob broke a rule: Ship would extend beyond grid\n", output)

    def test_can_place_ships_for_player(self):
        s5 = Ship("Carrier").set_location([
            Coordinates({'x': 'D', 'y': '5'}),
            Coordinates({'x': 'D', 'y': '6'}),
            Coordinates({'x': 'D', 'y': '7'}),
            Coordinates({'x': 'D', 'y': '8'}),
            Coordinates({'x': 'D', 'y': '9'})
        ])
        fake_input = mock.Mock(side_effect=['E', '5', 'h', 'A', '2', 'v', 'H', '4', 'h', 'B', '0', 'v', 'D', '5', 'h'])
        with patch('builtins.input', fake_input):
            player = Player()
            self.battleship.place_ships(player)
            self.assertEqual(player.grid.ships[4].location, s5.location)

    def test_can_place_ships_for_ai(self):
        player = Player(is_ai=True)
        self.battleship.place_ships(player)
        self.assertEqual(len(player.grid.ships), 5)

    def test_players_can_take_a_turn(self):
        self.add_players()
        fake_input = mock.Mock(side_effect=['E', '5', 'E', '5', 'F', '5'])
        with patch('builtins.input', fake_input):
            turn = self.battleship.take_a_turn(self.battleship.players[0], self.battleship.players[1])
            self.assertTrue(turn in self.battleship.turns)
            self.assertTrue(turn.shot, Shot(Coordinates({'x': 'E', 'y': '5'})))
            turn = self.battleship.take_a_turn(self.battleship.players[0], self.battleship.players[1])
            self.assertTrue(turn in self.battleship.turns)
            self.assertTrue(turn.shot, Shot(Coordinates({'x': 'F', 'y': '5'})))

    def test_battleship_can_play_a_round(self):
        self.add_players()
        fake_input = mock.Mock(side_effect=['B', '2', 'E', '5'])
        with patch('builtins.input', fake_input):
            self.battleship.play_a_round()
            self.assertEqual(len(self.battleship.turns), 2)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_battleship_can_start_battle_until_all_oppenent_ships_are_destroyed(self, mock_stdout):
        self.add_players()
        fake_input = mock.Mock(side_effect=['B', '2', 'C', '2', 'B', '3'])
        with patch('builtins.input', fake_input):
            self.battleship.battle_until_one_is_defeated()
            self.assertEqual(len(self.battleship.turns), 5)
            output = mock_stdout.getvalue()
            self.assertIn('Bob is victorious!\n', output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_battleship_can_play_an_ai_game_by_itself(self, mock_stdout):
        self.battleship.play_a_game(ai_v_ai=True)
        output = mock_stdout.getvalue()
        self.assertIn('AI is victorious!\n', output)


if __name__ == '__main__':
    unittest.main()
