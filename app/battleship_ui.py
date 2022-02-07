from player import Player


class BattleshipUI:

    def get_name(self):
        name = input('What is player\'s name? ')
        return name

    def warn(self, player: Player, warning: str):
        print(f'{player.name} broke a rule: {warning}')

    def place_ship(self, ship_model: str, player: Player):
        x = input(f'Please enter an x coordinate (A-J) to place {player.name}\'s {ship_model}: ')
        y = input('Please enter a y coordinate 1-10) to place {player.name}\'s {ship_model}: ')
        orientation = input(f'Please enter the {ship_model}\'s orientation (\'h\' for horizontal or \'v\' for vertical): ')
        coordinates = {'x': x, 'y': y}
        return coordinates, orientation

    def get_shot(self, player: Player):
        x = input(f'Please enter an x coordinate (A-J) to target {player.name}\'s opponent: ')
        y = input('Please enter a y coordinate (1-10) to target {player.name}\'s opponent: ')
        coordinates = {'x': x, 'y': y}
        return coordinates

    def announce_winner(self, player: Player):
        print(f'{player.name} is victorious!')