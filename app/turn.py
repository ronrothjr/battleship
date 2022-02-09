from player import Player
from shot import Shot


class Turn:

    def __init__(self, player: Player=None, shot: Shot=None, load: dict=None) -> None:
        if load:
            self.player = load['player']
            self.shot = Shot(load=load['shot'])
        else:
            self.player = player
            self.shot = shot