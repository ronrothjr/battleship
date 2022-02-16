from storage import Storage
from session import Session
from ui import UI


class Menu:

    def __init__(self, game: Storage=None) -> None:
        self.storage = game if game else Storage()
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
            'w': {
                'menu_choice': '(W)atch a Game',
                'action': self.watch_a_game
            },
            'e': {
                'menu_choice': '(E)xit',
                'action': lambda: True
            }
        }

    def display_main_menu(self):
        menu_choice = ''
        while not menu_choice.lower() == 'e':
            menu_choice = self.ui.get_menu_choice('Main Menu', self.options)
            option = self.options[menu_choice.lower()]
            option['action']()

    def play_a_game(self):
        game = Session(self.ui).play_a_new_game()
        if game:
            self.storage.save_a_game(game)

    def load_a_game(self):
        games = self.storage.load_a_game()
        options = self.get_game_choices(games)
        menu_choice = ''
        menu_choice = self.ui.get_menu_choice('Saved Games', options)
        if menu_choice == '0':
            return
        else:
            option = options[menu_choice.lower()]
            option['action'](menu_choice)

    def watch_a_game(self):
        Session(self.ui).play_a_new_game(ai_v_ai=True, watch=True)

    def get_game_choices(self, games):
        options = {'0': {'menu_choice': '(0) - Exit to Main Menu', 'action': lambda x: True}}
        keys = list(games.keys())
        if keys:
            keys.reverse()
            keys = keys[0:20]
            x = 1
            for timestamp in keys:
                game = games[timestamp]
                p1 = game["players"][0]["name"]
                p2 = game["players"][1]["name"]
                item = f'({x}) - {p1} v {p2} ({timestamp})'
                options[str(x)] = {
                    'menu_choice': item,
                    'action': lambda x: self.play_a_saved_game(games[timestamp])
                }
                x += 1
        return options

    def play_a_saved_game(self, game):
            session = Session(self.ui)
            session.load_a_saved_game(game)
            game = session.play_a_loaded_game()
            if game: 
                self.game.save_a_game(game)

if __name__ == '__main__':
    Menu().display_main_menu()
