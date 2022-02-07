from coordinates import Coordinates
from battleship_ui import BattleshipUI
from player import Player
from shot import Shot
from turn import Turn


class Battleship:

    def __init__(self) -> None:
        self.ui = BattleshipUI()
        self.players = []
        self.turns = []

    def set_players(self, players: list[Player]):
        self.players = players
        return self

    def set_turns(self, turns: list[Turn]):
        self.turns = turns
        return self

    def add_a_player(self, player: Player):
        self.players.append(player)

    def start_battle(self):
        is_battle_decided = False
        while not is_battle_decided:
            self.play_a_round()
            is_battle_decided = list(filter(lambda player: player.is_defeated(), self.players))

    def play_a_round(self):
        p1 = self.players[0]
        p2 = self.players[1]
        self.take_a_turn(p1, p2)
        if not p2.is_defeated():
            self.take_a_turn(p2, p1)

    def take_a_turn(self, player: Player, opponent: Player):
        shot = None
        is_shot_already_taken = True
        while is_shot_already_taken:
            x_y = self.ui.get_shot(player)
            coordinates = Coordinates(x_y)
            shot = Shot(coordinates)
            is_shot_already_taken = opponent.grid.is_shot_already_taken(shot)
        opponent.take_a_shot(shot)
        turn = Turn(player, shot)
        self.turns.append(turn)
        return turn