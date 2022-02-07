from player import Player
from shot import Shot


class Turn:

    def __init__(self, player: Player, shot: Shot) -> None:
        self.player = player
        self.shot = shot