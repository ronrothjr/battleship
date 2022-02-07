from functools import reduce
from coordinates import Coordinates
from grid import Grid
from player import Player
from shot import Shot


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

    def display_grids(self, player: Player, opponent: Player):
        ocean_grid = player.grid.get_all_ship_coordinates()
        target_grid = opponent.grid.get_all_shots_taken()
        print(f'\t{"-" * 45}\t\t{"-" * 45}')
        print('\t\t\tOcean Grid:\t\t\t\t\t\tTarget Grid:')
        print(f'\t{"-" * 45}\t\t{"-" * 45}')
        row = reduce(lambda row, y: f'{row} | {y}', Grid.y)
        print(f'\t|   | {row} |\t\t|   | {row} |')
        for x in Grid.x:
            ocean = ''
            target = ''
            for y in Grid.y:
                ocean += f' {self.get_grid_content(ocean_grid, x, y)} |'
            for y in Grid.y:
                target += f' {self.get_grid_content(target_grid, x, y, shots=True)} |'
            print(f'\t| {x} |{ocean}\t\t| {x} |{target}')
        print(f'\t{"-" * 45}\t\t{"-" * 45}')

    def get_grid_content(self, ships: list[Coordinates], x, y, shots=False):
        cell = Coordinates({'x': x, 'y': y})
        for coordinates in ships:
            if cell == coordinates:
                if shots:
                    return 'X' if coordinates.hit else '*'
                else:
                    return 'X' if coordinates.hit else 'O'
        return ' '

    def get_shot(self, player: Player):
        x = input(f'Please enter an x coordinate (A-J) to target {player.name}\'s opponent: ')
        y = input('Please enter a y coordinate (1-10) to target {player.name}\'s opponent: ')
        coordinates = {'x': x, 'y': y}
        return coordinates

    def announce_hit(self, player: Player, shot: Shot):
        print(f'{player.name} has scored a hit on a {shot.model}!')

    def announce_sunk(self, player: Player, shot: Shot):
        print(f'{player.name} has sunk a {shot.model}!')

    def announce_winner(self, player: Player):
        print(f'{player.name} is victorious!')