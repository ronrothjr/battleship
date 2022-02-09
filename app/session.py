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
            cancelled = self.place_ships(player)
            if cancelled:
                return False
        is_battle_decided = self.battle_until_one_is_defeated()
        if is_battle_decided:
            self.display_game_result()
            self.ui.input()
        self.ui.clear()
        return self

    def load_a_saved_game(self, game):
        self.timestamp = game['timestamp']
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
        is_battle_decided = self.battle_until_one_is_defeated()
        if is_battle_decided:
            self.display_game_result()
            self.ui.input()
        self.ui.clear()
        return self

    def add_a_player(self, player: Player):
        if not player.is_ai:
            player.name = self.ui.get_name()
        self.players.append(player)

    def place_ships(self, player: Player):
        for model in Ship.models():
            ocean_grid = player.grid.get_all_ship_coordinates()
            ship_added = False
            while not ship_added:
                x_y, orientation = self.ai.place_ship(model, player) if player.is_ai else self.ui.place_ship(model, player, ocean_grid, 'Ocean Grid')
                cancelled = isinstance(x_y, bool)
                if cancelled:
                    return True
                location = Grid.get_location_coordinates(model, x_y, orientation)
                if not location:
                    if not player.is_ai:
                        self.ui.warn(player, 'Ship would extend beyond grid')
                    continue
                ship = Ship(model).set_location(location)
                ship_added = player.grid.add_ship(ship)
                if not ship_added and not player.is_ai:
                    self.ui.warn(player, 'Ship would overlap other ships')
        return False

    def battle_until_one_is_defeated(self):
        is_battle_decided = False
        battle_is_paused = False
        while not is_battle_decided and not battle_is_paused:
            battle_is_paused = self.play_a_round()
            is_battle_decided = list(filter(lambda player: player.is_defeated(), self.players))
        return is_battle_decided

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
            self.ui.display_grids(player)
        shot = None
        shot_is_unverified = True
        while shot_is_unverified:
            x_y = self.ai.get_shot(player) if player.is_ai else self.ui.get_shot(player)
            if isinstance(x_y, bool):
                return True
            coordinates = Coordinates(x_y)
            shot = Shot(coordinates)
            shot_is_unverified = player.grid.is_shot_already_taken(shot)
        turn = self.record_the_shot_and_add_the_turn(player, opponent, shot)
        return turn

    def record_the_shot_and_add_the_turn(self, player: Player, opponent: Player, shot: Shot):
        shot = opponent.take_a_shot(shot)
        p1_or_p2 = 'p1' if player == self.players[0] else 'p2'
        ship_model = shot.model if shot.model and opponent.is_sunk(shot.model) else ''
        player.grid.add_shot(shot)
        self.ui.announce_hit(player, shot, p1_or_p2)
        self.ui.announce_sunk(player, ship_model, p1_or_p2)
        turn = Turn(player, shot)
        self.turns.append(turn)
        if (self.watch):
            time.sleep(2)
        return turn

    def display_game_result(self):
        winner = self.players[0] if self.players[1].is_defeated() else self.players[1]
        self.ui.display_grids(winner)
        rounds = int(int(len(self.turns)+1)/2)
        self.ui.announce_winner(winner, rounds, 'p1' if winner == self.players[0] else 'p2')


if __name__ == '__main__':
    Session().play_a_game(ai_v_ai=True, watch=True, orientation='portrait')