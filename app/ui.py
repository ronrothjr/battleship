from functools import reduce
from coordinates import Coordinates
from grid import Grid
from player import Player
from shot import Shot


class UI:

    def __init__(self, orientation='landscape'):
        self.spacing = 10
        self.grid_width = 45
        self.orientation = orientation

    def get_name(self):
        name = input('\n\tWhat is player\'s name? ')
        return name

    def validate_coordinates(self, text_input: str):
        x = text_input[0:1].upper()
        y = text_input[1:2]
        if x in Grid.x and y in Grid.y:
            return {'x': x, 'y': y}

    def prompt_for_valid_coordinates(self, prompt: str):
        coordinates = None
        while not coordinates:
            text_input = input(prompt)
            if text_input.lower() in ['exit', 'e', 'quit', 'q']:
                return True
            coordinates = self.validate_coordinates(text_input)
        return coordinates

    def display_output(self, message: str, display_width: int=None):
        if not display_width:
            display_width = ( self.grid_width * 2 ) + self.spacing if self.orientation == 'landscape' else self.grid_width
        output = self.center(message, display_width)
        return f'\t{output}'

    def center(self, message: str, display_width: int):
        padding = int( ( display_width - len(message) ) / 2) if display_width - len(message) > 0 else 0
        centered = (' ' * padding) + message
        return centered

    def warn(self, player: Player, warning: str):
        message = f'{player.name} broke a rule: {warning}'
        output = self.display_output(message, 45)
        print(output)

    def place_ship(self, ship_model: str, player: Player):
        coordinates = self.prompt_for_valid_coordinates(f'Please enter a coordinates (A1-J0) to place {player.name}\'s {ship_model}: ')
        orientation = input(f'Please enter the {ship_model}\'s orientation (\'h\' for horizontal or \'v\' for vertical): ')
        return coordinates, orientation

    def display_grid(self, ocean_grid: list[Coordinates], title: str, shots=False):
        print(f'\t{"-" * 45}')
        print(f'\t\t\t{title}:')
        print(f'\t{"-" * 45}')
        row = reduce(lambda row, y: f'{row} | {y}', Grid.y)
        print(f'\t|   | {row} |')
        for x in Grid.x:
            ocean = ''
            for y in Grid.y:
                ocean += f' {self.get_grid_content(ocean_grid, x, y, shots)} |'
            print(f'\t| {x} |{ocean}')
        print(f'\t{"-" * 45}')

    def display_grids(self, player: Player, opponent: Player):
        if self.orientation == 'landscape':
            self.display_grids_landscape(player, opponent)
        else:
            self.display_grids_portrait(player, opponent)

    def display_grids_landscape(self, player: Player, opponent: Player):
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

    def display_grids_portrait(self, player: Player, opponent: Player):
        ocean_grid = player.grid.get_all_ship_coordinates()
        target_grid = opponent.grid.get_all_shots_taken()
        self.display_grid(ocean_grid, 'Ocean Grid')
        self.display_grid(target_grid, 'Target Grid', shots=True)

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
        coordinates = self.prompt_for_valid_coordinates(f'Please enter coordinates (A1-J0) to target {player.name}\'s opponent: ')
        return coordinates

    def announce_hit(self, player: Player, shot: Shot):
        text = self.display_output(f'{player.name} has scored a hit on a {shot.model}!')
        print(text)

    def announce_sunk(self, player: Player, shot: Shot):
        text = self.display_output(f'{player.name} has sunk a {shot.model}!')
        print(text)

    def announce_winner(self, player: Player, rounds: int):
        text = self.display_output(f'{player.name} is victorious!')
        print(text)
        text = self.display_output(f'(in {rounds} rounds)')
        print(text)