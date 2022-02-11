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

    def __init__(self, ui: UI=None) -> None:
        self.timestamp = datetime.datetime.today().strftime("%Y%m%d%H%M%S")
        self.watch = False
        self.ai = AI()
        self.ui = ui if ui else UI()
        self.players = []
        self.turns = []

    def play_a_new_game(self, ai_v_ai=False, watch=False, orientation='portrait'):
        ready_to_play = self.setup_new_game(ai_v_ai, watch, orientation)
        return self.play_a_loaded_game(ready_to_play)

    def setup_new_game(self, ai_v_ai=False, watch=False, orientation='portrait'):
        self.ui.clear()
        self.watch = watch
        self.ui.orientation = orientation
        players = [True, True] if ai_v_ai else [False, True]
        for is_ai in players:
            player = Player(is_ai=is_ai)
            added = self.add_a_player(player)
            if not added:
                return None
            added = self.place_ships(player)
            if not added:
                return None
        return True

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

    def play_a_loaded_game(self, ready_to_play: bool=True):
        if ready_to_play:
            self.ui.clear()
            is_battle_paused = self.battle_until_one_is_defeated()
            if not is_battle_paused:
                self.display_game_result()
        return self

    def add_a_player(self, player: Player):
        if not player.is_ai:
            player.name = self.ui.get_name()
            if not player.name:
                return None
        self.players.append(player)
        return player

    def place_ships(self, player: Player):
        for model in Ship.models():
            ocean_grid = player.grid.get_all_ship_coordinates()
            self.ui.display_grid(ocean_grid, 'Ocean Grid')
            ship_added = False
            while not ship_added:
                x_y, orientation = self.ai.place_ship() if player.is_ai else self.ui.place_ship(model, player, ocean_grid, 'Ocean Grid')
                if not x_y:
                    return None
                location = Grid.get_location_coordinates(model, x_y, orientation)
                if not location:
                    if not player.is_ai:
                        self.ui.warn(player, 'Ship would extend beyond grid')
                    continue
                ship = Ship(model).set_location(location)
                ship_added = player.grid.add_ship(ship)
                if not ship_added and not player.is_ai:
                    self.ui.warn(player, 'Ship would overlap other ships')
        return player

    def battle_until_one_is_defeated(self):
        is_battle_decided = False
        battle_is_paused = False
        while not is_battle_decided and not battle_is_paused:
            battle_is_paused = self.play_a_round()
            is_battle_decided = list(filter(lambda player: player.is_defeated(), self.players))
        return battle_is_paused

    def play_a_round(self):
        battle_is_paused = False
        p1 = self.players[0]
        p2 = self.players[1]
        if p1.is_defeated() or p2.is_defeated():
            battle_is_paused = True
        if not p1.is_defeated() and not battle_is_paused:
            turn = self.take_a_turn(p1, p2)
            battle_is_paused = not turn
        if not p2.is_defeated() and not battle_is_paused:
            turn = self.take_a_turn(p2, p1)
            battle_is_paused = not turn
        return battle_is_paused

    def take_a_turn(self, player: Player, opponent: Player):
        is_time_to_display_grids = not player.is_ai or self.watch
        if is_time_to_display_grids:
            self.ui.display_grids(player)
        if (self.watch):
            time.sleep(2)
        shot = self.get_verified_shot(player, opponent)
        if not shot:
            return None
        turn = self.record_turn(player, opponent, shot)
        self.announce_turn_results(player, opponent, shot)
        return turn

    def get_verified_shot(self, player: Player, opponent: Player):
        shot = None
        shot_is_unverified = True
        while shot_is_unverified:
            x_y = self.ai.get_shot(player, opponent) if player.is_ai else self.ui.get_shot(player)
            if not x_y:
                return None
            coordinates = Coordinates(x_y)
            shot = Shot(coordinates)
            shot_is_unverified = player.grid.is_shot_already_taken(shot)
        return shot

    def record_turn(self, player: Player, opponent: Player, shot: Shot):
        shot = opponent.take_a_shot(shot)
        player.grid.add_shot(shot)
        turn = Turn(player, shot)
        self.turns.append(turn)
        return turn

    def announce_turn_results(self, player: Player, opponent: Player, shot: Shot):
        p1_or_p2 = 'p1' if player == self.players[0] else 'p2'
        self.ui.announce_hit(player, shot, p1_or_p2)
        model = shot.model if shot.model and opponent.is_sunk(shot.model) else ''
        self.ui.announce_sunk(player, model, p1_or_p2)

    def display_game_result(self):
        winner = self.players[0] if self.players[1].is_defeated() else self.players[1]
        self.ui.display_grids(winner)
        rounds = int(int(len(self.turns)+1)/2)
        self.ui.announce_winner(winner, rounds)


if __name__ == '__main__':
    Session().play_a_new_game(ai_v_ai=True, watch=True, orientation='portrait')
