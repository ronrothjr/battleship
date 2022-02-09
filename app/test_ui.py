import io, unittest
from unittest import mock
from unittest.mock import patch
from coordinates import Coordinates
from session import Session
from ui import UI
from player import Player
from shot import Shot


class TestUI(unittest.TestCase):

    def setUp(self) -> None:
        self.maxDiff = None
        self.ui = UI()

    def test_can_instantiate_a_ui(self):
        self.assertIsInstance(self.ui, UI)
        self.assertIsInstance(self.ui.spacing, int)
        self.assertIsInstance(self.ui.grid_width, int)
        self.assertIsInstance(self.ui.orientation, str)
        self.assertEqual(self.ui.get_name.__name__, 'get_name') 
        self.assertTrue(callable(self.ui.get_name))
        self.assertEqual(self.ui.validate_coordinates.__name__, 'validate_coordinates') 
        self.assertTrue(callable(self.ui.validate_coordinates))
        self.assertEqual(self.ui.prompt_for_valid_coordinates.__name__, 'prompt_for_valid_coordinates') 
        self.assertTrue(callable(self.ui.prompt_for_valid_coordinates))
        self.assertEqual(self.ui.display_output.__name__, 'display_output') 
        self.assertTrue(callable(self.ui.display_output))
        self.assertEqual(self.ui.center.__name__, 'center') 
        self.assertTrue(callable(self.ui.center))
        self.assertEqual(self.ui.warn.__name__, 'warn') 
        self.assertTrue(callable(self.ui.warn))
        self.assertEqual(self.ui.place_ship.__name__, 'place_ship') 
        self.assertTrue(callable(self.ui.place_ship))
        self.assertEqual(self.ui.display_grid.__name__, 'display_grid') 
        self.assertTrue(callable(self.ui.display_grid))
        self.assertEqual(self.ui.display_grids.__name__, 'display_grids') 
        self.assertTrue(callable(self.ui.display_grids))
        self.assertEqual(self.ui.get_shot.__name__, 'get_shot') 
        self.assertTrue(callable(self.ui.get_shot))
        self.assertEqual(self.ui.announce_hit.__name__, 'announce_hit') 
        self.assertTrue(callable(self.ui.announce_hit))
        self.assertEqual(self.ui.announce_sunk.__name__, 'announce_sunk') 
        self.assertTrue(callable(self.ui.announce_sunk))
        self.assertEqual(self.ui.announce_winner.__name__, 'announce_winner') 
        self.assertTrue(callable(self.ui.announce_winner))

    def test_ui_can_get_player_name(self):
        fake_input = mock.Mock(side_effect=['Ahab'])
        with patch('builtins.input', fake_input):
            name = self.ui.get_name()
            self.assertEqual(name, 'Ahab')

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_ui_can_warn_player_of_rules_violation(self, mock_stdout):
        self.ui.warn(Player(), 'Don\'t piss in the wind!')
        output = mock_stdout.getvalue()
        self.assertEqual(output, '\t  Bob broke a rule: Don\'t piss in the wind!\n')

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_ui_can_get_ship_placement_coordinates_and_orientation(self, mock_stdout):
        fake_input = mock.Mock(side_effect=['E5','h'])
        with patch('builtins.input', fake_input):
            x_y_dict, orientation = self.ui.place_ship('Destroyer', Player())
            self.assertEqual(x_y_dict, {'x': 'E', 'y': '5'})
            self.assertEqual(orientation, 'h')

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_ui_can_display_grids_for_player_and_opponent_view(self, mock_stdout):
        session = Session()
        session.players = [Player(is_ai=True), Player(is_ai=True)]
        p1 = session.players[0]
        p2 = session.players[1]
        session.place_ships(p1)
        session.place_ships(p2)
        self.ui.display_grids(p1, p2)
        output = mock_stdout.getvalue()
        self.assertIn(f'\t{"-" * 45}\t\t{"-" * 45}\n\t\t\tOcean Grid:\t\t\t\t\t\tTarget Grid:\n\t{"-" * 45}\t\t{"-" * 45}\n', output)

    def test_ui_can_get_a_shot_from_a_player(self):
        fake_input = mock.Mock(side_effect=['E5'])
        with patch('builtins.input', fake_input):
            x_y_dict = self.ui.get_shot(Player())
            self.assertEqual(x_y_dict, {'x': 'E', 'y': '5'})

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_ui_can_announce_a_hit(self, mock_stdout):
        coordinates = Coordinates({'x': 'B', 'y': '5'})
        coordinates.hit = True
        shot = Shot(Coordinates)
        shot.hit = True
        shot.model = 'Battleship'
        self.ui.announce_hit(Player(), shot)
        output = mock_stdout.getvalue()
        self.assertEqual(output, f'\t{" " * 31}Bob has scored a hit on a Battleship!\n')

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_ui_can_announce_winner(self, mock_stdout):
        self.ui.announce_winner(Player(), 25)
        output = mock_stdout.getvalue()
        self.assertEqual(output, f'\t{" " * 41}Bob is victorious!\n\t{" " * 43}(in 25 rounds)\n')



if __name__ == '__main__':
    unittest.main()
