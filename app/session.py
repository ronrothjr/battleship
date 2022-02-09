import datetime, time
from ai import AI
from coordinates import Coordinates
from game import Game
from grid import Grid
from player import Player
from ship import Ship
from shot import Shot
from turn import Turn
from ui import UI


class Session:

    def __init__(self) -> None:
        self.timestamp = datetime.datetime.today().strftime("%Y%m%d%H%M%S")
        self.watch = False
        self.data = Game()
        self.ai = AI()
        self.ui = UI()
        self.players = []
        self.turns = []

    def play_a_game(self, ai_v_ai=False, watch=False, orientation='portrait'):
        self.watch = watch
        self.ui.orientation = orientation
        players = [True, True] if ai_v_ai else [False, True]
        for is_ai in players:
            player = Player(is_ai=is_ai)
            self.add_a_player(player)
            self.place_ships(player)
        self.battle_until_one_is_defeated()
        self.display_game_result()
        return self

    def load_a_saved_game(self, game):
        self.timestamp = game['timestamp']
        self.ui.orientation = game['ui']['orientation']
        self.set_players(game['players'])
        self.set_turns(game['turns'])

    def set_players(self, players: list[dict]):
        self.players = [Player(load=p) for p in players]
        return self

    def set_turns(self, turns: list[dict]):
        turn_count = 0
        p1 = self.players[0]
        p2 = self.players[1]
        for t in turns:
            t['player'] = p1 if turn_count % 2 == 0 else p2
            turn_count += 1
            self.turns.append(Turn(load=t))
        return self

    def play_a_loaded_game(self):
        self.battle_until_one_is_defeated()
        self.display_game_result()
        return self

    def add_a_player(self, player: Player):
        if not player.is_ai:
            player.name = self.ui.get_name()
        self.players.append(player)

    def place_ships(self, player: Player):
        for model in Ship.models():
            ocean_grid = player.grid.get_all_ship_coordinates()
            self.ui.display_grid(ocean_grid, 'Ocean Grid')
            ship_added = False
            while not ship_added:
                x_y, orientation = self.ai.place_ship(model, player) if player.is_ai else self.ui.place_ship(model, player)
                location = Grid.get_location_coordinates(model, x_y, orientation)
                if not location:
                    if not player.is_ai:
                        self.ui.warn(player, 'Ship would extend beyond grid')
                    continue
                ship = Ship(model).set_location(location)
                ship_added = player.grid.add_ship(ship)
                if not ship_added and not player.is_ai:
                    self.ui.warn(player, 'Ship would overlap other ships')

    def battle_until_one_is_defeated(self):
        is_battle_decided = False
        battle_is_paused = False
        while not is_battle_decided and not battle_is_paused:
            battle_is_paused = self.play_a_round()
            is_battle_decided = list(filter(lambda player: player.is_defeated(), self.players))

    def play_a_round(self):
        battle_is_paused = False
        p1 = self.players[0]
        p2 = self.players[1]
        if p1.is_defeated() or p2.is_defeated():
            battle_is_paused = True
        if not p1.is_defeated() and not battle_is_paused:
            turn = self.take_a_turn(p1, p2)
            battle_is_paused = isinstance(turn, bool)
        if not p2.is_defeated() and not battle_is_paused:
            turn = self.take_a_turn(p2, p1)
            battle_is_paused = isinstance(turn, bool)
        return battle_is_paused

    def take_a_turn(self, player: Player, opponent: Player):
        if not player.is_ai or self.watch:
            self.ui.display_grids(player, opponent)
        if (self.watch):
            time.sleep(2)
        shot = None
        shot_is_unverified = True
        while shot_is_unverified:
            x_y = self.ai.get_shot(opponent) if player.is_ai else self.ui.get_shot(player)
            if isinstance(x_y, bool):
                return True
            coordinates = Coordinates(x_y)
            shot = Shot(coordinates)
            shot_is_unverified = opponent.grid.is_shot_already_taken(shot)
        shot = opponent.take_a_shot(shot)
        if shot.hit:
            self.ui.announce_hit(player, shot)
            if player.is_sunk(shot.model):
                self.ui.announce_sunk(player, shot)
        turn = Turn(player, shot)
        self.turns.append(turn)
        return turn

    def display_game_result(self):
        winner = self.players[0] if self.players[1].is_defeated() else self.players[1]
        loser = self.players[1] if self.players[1].is_defeated() else self.players[0]
        self.ui.display_grids(winner, loser)
        rounds = int(int(len(self.turns)+1)/2)
        self.ui.announce_winner(winner, rounds)


if __name__ == '__main__':
    Session().play_a_game(ai_v_ai=True, watch=True, orientation='portrait')