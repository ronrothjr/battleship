from player import Player


class Battleship:

    def __init__(self) -> None:
        self.players = []

    def add_player(self, player: Player):
        self.players.append(player)