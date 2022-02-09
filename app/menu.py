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
            prompt = '\tChoose an option: '
            menu_choice = input(prompt)
            if menu_choice.lower() not in choices:
                print(f'\n\tPlease choose an option ({", ".join(choices)})')
                menu_choice = None
        return menu_choice

    def display_main_menu(self):
        menu_choice = ''
        while not menu_choice.lower() == 'e':
            output = self.ui.display_output('Main Menu', 45)
            print(output)
            for v in self.options.values():
                output = self.ui.display_output(v['menu_choice'], 45)
                print(output)
            menu_choice = self.get_menu_choice()
            option = self.options[menu_choice.lower()]
            option['action']()

    def play_a_game(self):
        game = Session().play_a_game()
        self.game.save_a_game(game)

    def load_a_game(self):
        output = self.ui.display_output('Saved Games', 45)
        print(output)
        output = self.ui.display_output('(0) - Exit to Main Menu', 45)
        print(output)
        games = self.game.load_a_game()
        for x in range(0, len(games)):
            game = games[x]
            p1 = game["players"][0]["name"]
            p2 = game["players"][1]["name"]
            timestamp = game["timestamp"]
            item = f'({x + 1}) - {p1} v {p2} ({timestamp})'
            output = self.ui.display_output(item, 45)
            print(output)
        game_choice = self.get_loaded_game_choice(games)
        if game_choice == 0:
            return
        else:
            game_to_play = games[game_choice - 1]
            self.play_a_saved_game(game_to_play)

    def play_a_saved_game(self, game):
            session = Session()
            session.load_a_saved_game(game)
            session.play_a_loaded_game()

    def get_loaded_game_choice(self, games):
        game_choice = None
        while not game_choice:
            prompt = '\tChoose an game: '
            game_choice = input(prompt)
            if int(game_choice) not in range(0, len(games) + 2):
                print(f'\n\tPlease choose a game (0-{len(games) + 1})')
                game_choice = None
        return int(game_choice)

if __name__ == '__main__':
    Menu().display_main_menu()
