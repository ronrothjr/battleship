from player import Player


class BattleshipUI:

    def get_shot(self, player: Player):
        x = input(f'Please enter an x coordinate to target {player.name}\'s opponent: ')
        y = int(input('Please enter an y coordinate to target {player.name}\'s opponent: '))
        coordinates = {'x': x, 'y': y}
        return coordinates