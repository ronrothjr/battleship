import copy, os, re, sys, time
from turtle import pos
from pynput import keyboard
from functools import reduce
from coordinates import Coordinates
from grid import Grid
from player import Player
from ship import Ship
from shot import Shot


class UI:

    def __init__(self, orientation='portrait'):
        os.system('cls')
        self.position = {'x': 'E', 'y': '5'}
        self.size = 10
        self.spacing = 10
        self.grid_width = 45
        self.tab = ' ' * 8
        self.orientation = orientation
        self.input_buffer = ''
        self.response = ''
        self.cursor = '*'
        self.empty = ' '
        self.ship_model = None
        self.ship_orientation = None
        self.ship_location = None
        self.redisplay = None
        self.cursor_movement_handlers = {
            'Key.up': self.up,
            'Key.down': self.down,
            'Key.left': self.left,
            'Key.right': self.right,
            'Key.enter': self.enter,
            'Key.esc': self.esc,
            'Key.space': self.spacebar
        }
        self.listen_for_keyboard_events()

    def listen_for_keyboard_events(self):
        self.listener = keyboard.Listener(on_press=self.handle_keyboard_events)
        self.listener.start()

    def handle_keyboard_events(self, key):
        entered = str(key).replace("'", "")        
        if self.is_cursor_movement_key(entered):
            self.handle_cursor_movement(entered)
            self.display_board()
        if re.match('^[0-9]|[a-z]|[A-Z]$', entered):
            self.input_buffer += entered
            self.print_there(self.spacing, 0, f'{self.input_buffer}')

    def display_board(self):
        if self.redisplay:
            args = self.redisplay['args']
            self.redisplay['grid'](**args)

    def is_cursor_movement_key(self, key):
        list_of_cursor_movement_keys = list(self.cursor_movement_handlers.keys())
        return key in list_of_cursor_movement_keys

    def handle_cursor_movement(self, key):
        self.cursor_movement_handlers.get(key)()
        if self.ship_orientation:
            self.ship_location = Grid.get_location_coordinates(self.ship_model, self.position, self.ship_orientation)

    def up(self):
        x_index = Grid.x.index(self.position['x'])
        if x_index > 0:
            self.position['x'] = Grid.x[x_index - 1]

    def down(self):
        x_index = Grid.x.index(self.position['x'])
        if x_index < 9:
            self.position['x'] = Grid.x[x_index + 1]

    def left(self):
        y_index = Grid.y.index(self.position['y'])
        if y_index > 0:
            self.position['y'] = Grid.y[y_index - 1]
    
    def right(self):
        y_index = Grid.y.index(self.position['y'])
        if y_index < 9:
            self.position['y'] = Grid.y[y_index + 1]

    def enter(self):
        self.response = copy.copy(self.input_buffer)
        self.input_buffer = ''
        self.display_board()

    def esc(self):
        self.clear()
        self.response = 'exit'

    def clear(self):
        os.system('cls')

    def spacebar(self):
        if self.ship_orientation:
            self.ship_orientation = 'h' if self.ship_orientation == 'v' else 'v'
            self.input_buffer = self.ship_orientation
            self.print_there(self.spacing, 0, f'{self.input_buffer}')
        else:
            self.enter()

    def input(self):
        while not self.response:
            time.sleep(0.0)
        response = copy.copy(self.response)
        self.response = ''
        self.print_there(0, 0, f'{" " * self.grid_width * 2}')
        return response

    def print_there(self, x, y, text):
        sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (y, x, text))
        sys.stdout.flush()

    def get_name(self):
        prompt = self.display_output(f'What is player\'s name? ', self.grid_width)
        self.print_there(self.spacing, 3, prompt)
        name = self.input()
        return name

    def validate_coordinates(self, text_input: str):
        x = text_input[0:1].upper()
        y = text_input[1:2]
        if x in Grid.x and y in Grid.y:
            return {'x': x, 'y': y}

    def prompt_for_valid_coordinates(self):
        coordinates = None
        while not coordinates:
            text_input = self.input()
            if text_input.lower() in ['exit', 'e', 'quit', 'q', 'pause', 'p']:
                return True
            text_input = f'{self.position["x"]}{self.position["y"]}'
            coordinates = self.validate_coordinates(text_input)
        return coordinates

    def display_output(self, message: str, display_width: int=None):
        if not display_width:
            display_width = ( self.grid_width * 2 ) + self.spacing if self.orientation == 'landscape' else self.grid_width
        output = self.center(message, display_width)
        return f'{self.tab}{output}'

    def center(self, message: str, display_width: int):
        padding = int( ( display_width - len(message) ) / 2) if display_width - len(message) > 0 else 0
        centered = (' ' * padding) + message
        return centered

    def warn(self, player: Player, warning: str):
        message = f'{player.name} broke a rule: {warning}'
        output = self.display_output(message, self.grid_width)
        self.print_there(self.spacing, 2, output)

    def place_ship(self, ship_model: str, player: Player, ocean_grid: list[Coordinates], title: str):
        args = {'ocean_grid': ocean_grid, 'title': title, 'cursor': True}
        self.redisplay = {'grid': self.display_grid, 'args': args}
        self.display_grid(**args)
        self.ship_model = ship_model
        self.ship_orientation = 'h'
        self.ship_location = Grid.get_location_coordinates(self.ship_model, self.position, self.ship_orientation)
        self.input_buffer = self.ship_orientation
        self.print_there(self.spacing, 0, f'{self.input_buffer}')
        self.print_there(self.spacing, 2, ' ' * 110)
        self.print_there(self.spacing, 2, f'Please press enter to place {player.name}\'s {ship_model}')
        self.print_there(self.spacing, 3, ' ' * 110)
        self.print_there(self.spacing, 3, f'Use spacebar to change orientation (horizontal or vertical)')
        coordinates = self.prompt_for_valid_coordinates()
        if isinstance(coordinates, bool):
            return True, self.ship_orientation
        orientation = copy.copy(self.ship_orientation)
        self.ship_model = None
        self.ship_orientation = None
        self.ship_location = None
        self.redisplay = None
        self.print_there(self.spacing, 0, ' ' * 110)
        self.print_there(self.spacing, 1, ' ' * 110)
        self.print_there(self.spacing, 2, ' ' * 110)
        return coordinates, orientation

    def display_grid(self, ocean_grid: list[Coordinates], title: str, shots=False, offset: int=0, cursor: bool=False):
        self.print_there(offset + self.spacing, 4, f'{self.tab}{"-" * self.grid_width}')
        self.print_there(offset + self.spacing, 5, f'{self.tab}{self.tab}{self.tab}{title}:')
        self.print_there(offset + self.spacing, 6, f'{self.tab}{"-" * self.grid_width}')
        row = reduce(lambda row, y: f'{row} | {y}', Grid.y)
        self.print_there(offset + self.spacing, 7, f'{self.tab}|   | {row} |')
        grid = copy.copy(ocean_grid)
        grid += [] if self.ship_location is None else self.ship_location
        x_index = 0
        for x in Grid.x:
            x_index += 1
            ocean = ''
            for y in Grid.y:
                ocean += f'{self.get_grid_content(grid, x, y, shots, cursor)}|'
            self.print_there(offset + self.spacing, 7 + x_index, f'{self.tab}| {x} |{ocean}')
        self.print_there(offset + self.spacing, 18, f'{self.tab}{"-" * self.grid_width}')

    def display_grids(self, player: Player):
        ocean_grid = player.grid.get_all_ship_coordinates()
        target_grid = player.grid.get_all_shots_taken()
        cursor = not player.is_ai
        if self.orientation == 'landscape':
            self.display_grids_landscape(ocean_grid, target_grid, cursor)
        else:
            self.display_grids_portrait(ocean_grid, target_grid, cursor)

    def display_grids_landscape(self, ocean_grid: list[Coordinates], target_grid: list[Coordinates], cursor: bool=False):
        self.print_there(self.spacing, 4, f'{"-" * self.grid_width}{self.tab}{self.tab}{"-" * self.grid_width}')
        self.print_there(self.spacing, 5, '{self.tab}{self.tab}Ocean Grid:{self.tab}{self.tab}{self.tab}{self.tab}{self.tab}{self.tab}Target Grid:')
        self.print_there(self.spacing, 6, f'{"-" * self.grid_width}{self.tab}{self.tab}{"-" * self.grid_width}')
        row = reduce(lambda row, y: f'{row} | {y}', Grid.y)
        self.print_there(self.spacing, 7, f'|   | {row} |{self.tab}{self.tab}|   | {row} |')
        x_index = 0
        for x in Grid.x:
            x_index += 1
            ocean = ''
            target = ''
            for y in Grid.y:
                ocean += f'{self.get_grid_content(ocean_grid, x, y)}|'
            for y in Grid.y:
                target += f'{self.get_grid_content(target_grid, x, y, shots=True, cursor=True)}|'
            self.print_there(self.spacing, 7 + x_index, f'| {x} |{ocean}{self.tab}{self.tab}| {x} |{target}')
        self.print_there(self.spacing, 18, f'{"-" * self.grid_width}{self.tab}{self.tab}{"-" * self.grid_width}')
        args = {'ocean_grid': ocean_grid, 'target_grid': target_grid, 'cursor': cursor}
        self.redisplay = {'grid': self.display_grids_landscape, 'args': args}

    def display_grids_portrait(self, ocean_grid: list[Coordinates], target_grid: list[Coordinates], cursor: bool=False):
        self.display_grid(ocean_grid, 'Ocean Grid')
        args = {'ocean_grid': target_grid, 'title': 'Target Grid', 'shots': True, 'offset': 54, 'cursor': cursor}
        self.redisplay = {'grid': self.display_grid, 'args': args}
        self.display_grid(**args)

    def get_grid_content(self, ships: list[Coordinates], x, y, shots=False, cursor=False):
        contents = self.empty
        cell = Coordinates({'x': x, 'y': y})
        for coordinates in ships:
            if cell == coordinates:
                if shots:
                    contents = 'X' if coordinates.hit else '*'
                else:
                    contents = 'X' if coordinates.hit else 'O'
        if cursor and self.position['x'] == x and self.position['y'] == y:
            contents = f'[{contents}]'
        else:
            contents = f' {contents} '
        return contents

    def get_shot(self, player: Player):
        self.print_there(self.spacing, 3, ' ' * 110)
        self.print_there(self.spacing, 3, f'Please press Enter to target {player.name}\'s opponent: ')
        self.input_buffer = ' '
        coordinates = self.prompt_for_valid_coordinates()
        self.redisplay = None
        return coordinates

    def clear_announcements(self):
        self.print_there(self.spacing, 1, ' ' * 110)
        self.print_there(self.spacing, 2, ' ' * 110)
        self.print_there(self.spacing, 3, ' ' * 110)
        self.print_there(self.spacing, 20, ' ' * 110)
        self.print_there(self.spacing, 21, ' ' * 110)

    def announce_hit(self, player: Player, shot: Shot, p1_or_p2: str='p1'):
        self.print_there(self.spacing + (54 if p1_or_p2 == 'p2' else 0), 20, 50 * ' ')
        if shot.hit:
            text = self.display_output(f'{player.name} has scored a hit on a {shot.model}!')
            self.print_there(self.spacing + (54 if p1_or_p2 == 'p2' else 0), 20, text)

    def announce_sunk(self, player: Player, model: str, p1_or_p2: str='p1'):
        self.print_there(self.spacing + (54 if p1_or_p2 == 'p2' else 0), 21, 50 * ' ')
        if model:
            text = self.display_output(f'{player.name} has sunk a {model}!')
            self.print_there(self.spacing + (54 if p1_or_p2 == 'p2' else 0), 21, text)

    def announce_winner(self, player: Player, rounds: int, p1_or_p2: str='p1'):
        text = self.display_output(f'{player.name} is victorious!')
        self.print_there(self.spacing + (54 if p1_or_p2 == 'p2' else 0), 22, text)
        text = self.display_output(f'(in {rounds} rounds)')
        self.print_there(self.spacing + (54 if p1_or_p2 == 'p2' else 0), 23, text)