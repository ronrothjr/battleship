import io, unittest
from unittest import mock
from unittest.mock import patch
from app.coordinates import Coordinates
from battleship import Battleship
from battleship_ui import BattleshipUI
from player import Player
from shot import Shot


class TestBattleshipUI(unittest.TestCase):

    def setUp(self) -> None:
        self.maxDiff = None
        self.battleship_ui = BattleshipUI()

    def test_can_instantiate_a_battleship_ui(self):
        self.assertIsInstance(self.battleship_ui, BattleshipUI)
        self.assertEqual(self.battleship_ui.get_name.__name__, 'get_name') 
        self.assertTrue(callable(self.battleship_ui.get_name))
        self.assertEqual(self.battleship_ui.warn.__name__, 'warn') 
        self.assertTrue(callable(self.battleship_ui.warn))
        self.assertEqual(self.battleship_ui.place_ship.__name__, 'place_ship') 
        self.assertTrue(callable(self.battleship_ui.place_ship))
        self.assertEqual(self.battleship_ui.display_grid.__name__, 'display_grid') 
        self.assertTrue(callable(self.battleship_ui.display_grid))
        self.assertEqual(self.battleship_ui.display_grids.__name__, 'display_grids') 
        self.assertTrue(callable(self.battleship_ui.display_grids))
        self.assertEqual(self.battleship_ui.get_shot.__name__, 'get_shot') 
        self.assertTrue(callable(self.battleship_ui.get_shot))
        self.assertEqual(self.battleship_ui.announce_hit.__name__, 'announce_hit') 
        self.assertTrue(callable(self.battleship_ui.announce_hit))
        self.assertEqual(self.battleship_ui.announce_sunk.__name__, 'announce_sunk') 
        self.assertTrue(callable(self.battleship_ui.announce_sunk))
        self.assertEqual(self.battleship_ui.announce_winner.__name__, 'announce_winner') 
        self.assertTrue(callable(self.battleship_ui.announce_winner))

    def test_ui_can_get_player_name(self):
        fake_input = mock.Mock(side_effect=['Ahab'])
        with patch('builtins.input', fake_input):
            name = self.battleship_ui.get_name()
            self.assertEqual(name, 'Ahab')

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_ui_can_warn_player_of_rules_violation(self, mock_stdout):
        self.battleship_ui.warn(Player(), 'Don\'t piss in the wind!')
        output = mock_stdout.getvalue()
        self.assertEqual(output, 'Bob broke a rule: Don\'t piss in the wind!\n')

    def test_ui_can_get_ship_placement_coordinates_and_orientation(self):
        fake_input = mock.Mock(side_effect=['E','5','h'])
        with patch('builtins.input', fake_input):
            x_y_dict, orientation = self.battleship_ui.place_ship('Destroyer', Player())
            self.assertEqual(x_y_dict, {'x': 'E', 'y': '5'})
            self.assertEqual(orientation, 'h')

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_ui_can_display_grids_for_player_and_opponent_view(self, mock_stdout):
        battleship = Battleship()
        battleship.set_players([Player(is_ai=True), Player(is_ai=True)])
        p1 = battleship.players[0]
        p2 = battleship.players[1]
        battleship.place_ships(p1)
        battleship.place_ships(p2)
        self.battleship_ui.display_grids(p1, p2)
        output = mock_stdout.getvalue()
        self.assertIn(f'\t{"-" * 45}\t\t{"-" * 45}\n\t\t\tOcean Grid:\t\t\t\t\t\tTarget Grid:\n\t{"-" * 45}\t\t{"-" * 45}\n', output)

    def test_ui_can_get_a_shot_from_a_player(self):
        fake_input = mock.Mock(side_effect=['E','5'])
        with patch('builtins.input', fake_input):
            x_y_dict = self.battleship_ui.get_shot(Player())
            self.assertEqual(x_y_dict, {'x': 'E', 'y': '5'})

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_ui_can_announce_a_hit(self, mock_stdout):
        coordinates = Coordinates({'x': 'B', 'y': '5'})
        coordinates.hit = True
        shot = Shot(Coordinates)
        shot.hit = True
        shot.model = 'Battleship'
        self.battleship_ui.announce_hit(Player(), shot)
        output = mock_stdout.getvalue()
        self.assertEqual(output, 'Bob has scored a hit on a Battleship!\n')

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_ui_can_announce_winner(self, mock_stdout):
        self.battleship_ui.announce_winner(Player())
        output = mock_stdout.getvalue()
        self.assertEqual(output, 'Bob is victorious!\n')



if __name__ == '__main__':
    unittest.main()
