from coordinates import Coordinates
from battleship_ai import BattleshipAI
from battleship_ui import BattleshipUI
from grid import Grid
from player import Player
from ship import Ship
from shot import Shot
from turn import Turn


class Battleship:

    def __init__(self) -> None:
        self.ai = BattleshipAI()
        self.ui = BattleshipUI()
        self.players = []
        self.turns = []

    def set_players(self, players: list[Player]):
        self.players = players
        return self

    def set_turns(self, turns: list[Turn]):
        self.turns = turns
        return self

    def play_a_game(self, ai_v_ai=False):
        players = [True, True] if ai_v_ai else [False, True]
        for is_ai in players:
            player = Player(is_ai=is_ai)
            self.add_a_player(player)
            self.place_ships(player)
        self.battle_until_one_is_defeated()

    def add_a_player(self, player: Player):
        if not player.is_ai:
            player.name = self.ui.get_name()
        self.players.append(player)

    def place_ships(self, player: Player):
        for model in Ship.models():
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
        while not is_battle_decided:
            self.play_a_round()
            is_battle_decided = list(filter(lambda player: player.is_defeated(), self.players))
        self.ui.announce_winner(self.players[0] if self.players[1].is_defeated() else self.players[1])

    def play_a_round(self):
        p1 = self.players[0]
        p2 = self.players[1]
        self.take_a_turn(p1, p2)
        if not p2.is_defeated():
            self.take_a_turn(p2, p1)

    def take_a_turn(self, player: Player, opponent: Player):
        shot = None
        shot_is_unverified = True
        while shot_is_unverified:
            x_y = self.ai.get_shot(opponent) if player.is_ai else self.ui.get_shot(player)
            coordinates = Coordinates(x_y)
            shot = Shot(coordinates)
            shot_is_unverified = opponent.grid.is_shot_already_taken(shot)
        opponent.take_a_shot(shot)
        turn = Turn(player, shot)
        self.turns.append(turn)
        return turn