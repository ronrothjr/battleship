from time import time
from game import Game
from session import Session
from ui import UI


class Menu:

    def __init__(self, game: Game=None) -> None:
        self.game = game if game else Game()
        self.ui = UI()
        self.options = {
            'p': {
                'menu_choice': '(P)lay a Game',
                'action': self.play_a_game
            },
            'l': {
                'menu_choice': '(L)oad a Game',
                'action': self.load_a_game
            },
            'e': {
                'menu_choice': '(E)xit',
                'action': lambda: True
            }
        }

    def get_menu_choice(self):
        choices = [x for x in self.options.keys()]
        menu_choice = None
        while not menu_choice:
            prompt = self.ui.display_output(f'Please choose an option ({", ".join(choices)})', 45)
            self.ui.print_there(self.ui.spacing, 8, f'{prompt}')
            menu_choice = self.ui.input()
            if menu_choice.lower() not in choices:
                self.ui.print_there(self.ui.spacing, 8, f'{prompt}')
                menu_choice = None
        return menu_choice

    def display_main_menu(self):
        menu_choice = ''
        while not menu_choice.lower() == 'e':
            x = 2
            self.ui.clear()
            output = self.ui.display_output('Main Menu', 45)
            self.ui.print_there(self.ui.spacing, x, f'{output}')
            for v in self.options.values():
                x += 1
                output = self.ui.display_output(v['menu_choice'], 45)
                self.ui.print_there(self.ui.spacing, x, f'{output}')
            menu_choice = self.get_menu_choice()
            option = self.options[menu_choice.lower()]
            option['action']()

    def play_a_game(self):
        game = Session().play_a_game()
        if game:
            self.game.save_a_game(game)

    def load_a_game(self):
        self.ui.clear()
        output = self.ui.display_output('Saved Games', 45)
        self.ui.print_there(self.ui.spacing, 4, f'{output}')
        output = self.ui.display_output('(0) - Exit to Main Menu', 45)
        self.ui.print_there(self.ui.spacing, 5, f'{output}')
        games = self.game.load_a_game()
        x = 1
        keys = list(games.keys())
        if keys:
            keys.reverse()
            keys = keys[0:20]
            for timestamp in keys:
                game = games[timestamp]
                p1 = game["players"][0]["name"]
                p2 = game["players"][1]["name"]
                item = f'({x}) - {p1} v {p2} ({timestamp})'
                output = self.ui.display_output(item, 45)
                self.ui.print_there(self.ui.spacing, x + 5, f'{output}')
                x += 1
        game_choice = self.get_loaded_game_choice(keys)
        if game_choice == 0:
            return
        else:
            key_index = game_choice - 1
            timestamp = keys[key_index]
            game_to_play = games[timestamp]
            game = self.play_a_saved_game(game_to_play)
            if game: 
                self.game.save_a_game(game)

    def get_loaded_game_choice(self, keys):
        game_choice = None
        while not game_choice:
            prompt = self.ui.display_output(f'Please choose a game (0-{len(keys) + 1})', 45)
            self.ui.print_there(self.ui.spacing, 2, f'{prompt}')
            game_choice = self.ui.input()
            if int(game_choice) not in range(0, len(keys) + 2):
                self.ui.print_there(self.ui.spacing, 2, f'{prompt}')
                game_choice = None
        return int(game_choice)

    def play_a_saved_game(self, game):
            session = Session()
            session.load_a_saved_game(game)
            return session.play_a_loaded_game()

if __name__ == '__main__':
    Menu().display_main_menu()
