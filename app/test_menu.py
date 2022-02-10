import io, unittest
from unittest import mock
from unittest.mock import patch
from game import Game
from menu import Menu
from session import Session
from ui import UI
from data import Data
from files_mock import FilesMock


class TestMenu(unittest.TestCase):

    def setUp(self) -> None:
        self.menu = Menu(game=Game(data_store=Data(FilesMock())))

    def test_can_instantiate_a_menu(self):
        self.assertIsInstance(self.menu, Menu)
        self.assertIsInstance(self.menu.ui, UI)
        self.assertIsInstance(self.menu.game, Game)
        self.assertIsInstance(self.menu.options, dict)
        self.assertEqual(self.menu.display_main_menu.__name__, 'display_main_menu') 
        self.assertTrue(callable(self.menu.display_main_menu))
        self.assertEqual(self.menu.play_a_game.__name__, 'play_a_game') 
        self.assertTrue(callable(self.menu.load_a_game))
        self.assertEqual(self.menu.play_a_saved_game.__name__, 'play_a_saved_game') 
        self.assertTrue(callable(self.menu.play_a_saved_game))
        self.assertEqual(self.menu.load_a_game.__name__, 'load_a_game') 
        self.assertTrue(callable(self.menu.load_a_game))
        self.assertEqual(self.menu.get_menu_choice.__name__, 'get_menu_choice') 
        self.assertTrue(callable(self.menu.get_menu_choice))
        self.assertEqual(self.menu.get_loaded_game_choice.__name__, 'get_loaded_game_choice') 
        self.assertTrue(callable(self.menu.get_loaded_game_choice))

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_can_display_main_menu(self, mock_stdout):
        menu = Menu(game=Game(data_store=Data(FilesMock())))
        self.menu.ui.enter_text('E')
        menu.display_main_menu()
        output = mock_stdout.getvalue()
        self.assertIn('Main Menu', output)
        self.assertIn('(P)lay a Game', output)
        self.assertIn('(L)oad a Game', output)
        self.assertIn('(E)xit', output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_can_display_load_game_menu(self, mock_stdout):
        data_store = Data(FilesMock())
        game = Game(data_store=data_store)
        menu = Menu(game=game)
        games_str = '[{"watch": false, "ai": {}, "ui": {"spacing": 10, "grid_width": 45, "orientation": "portrait"}, "players": [{"name": "Bob"}, {"name": "AI"}], "turns": [], "timestamp": "20220208152345"}]'
        menu.game.data_store.files.files['games.txt'] = games_str
        fake_input = mock.Mock(side_effect=['0'])
        with patch('builtins.input', fake_input):
            menu.load_a_game()
            output = mock_stdout.getvalue()
            expected = f'\t{" " * 17}Saved Games\n\t{" " * 11}(0) - Exit to Main Menu\n\t{" " * 7}(1) - Bob v AI (20220208152345)\n'
            self.assertEqual(output, expected)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_can_display_load_game_menu_and_play_a_game(self, mock_stdout):
        data_store = Data(FilesMock())
        game = Game(data_store=data_store)
        def replace_play_a_game(x):
            game_result = Session().play_a_game(ai_v_ai=True)
            game.save_a_game(game_result)
        with mock.patch.object(Menu, 'play_a_game', replace_play_a_game):
            menu = Menu(game=game)
            fake_input = mock.Mock(side_effect=['P', 'L', '1', 'E'])
            with patch('builtins.input', fake_input):
                menu.display_main_menu()
                games = menu.game.data_store.files.files['games.txt']
                output = mock_stdout.getvalue()
                self.assertIn('AI is victorious', output)


if __name__ == '__main__':
    unittest.main()
