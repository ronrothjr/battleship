# import pygame
import threading, unittest
from game import Game
from mock_pygame import MockPygame
from director import Director
from event_publisher import EventPublisher
from scenes.settings import settings

        
class TestGame(unittest.TestCase):

    def setUp(self) -> None:
        self.game = Game(MockPygame()).on_init(settings)
        # self.game = Game(pygame)
        self.assertTrue(self.game._running)
        threading.Timer(0.1, self.game.pg.event.post, [self.game.pg.event.Event(self.game.pg.QUIT)]).start()
        self.game.start()

    def tearDown(self) -> None:
        self.assertFalse(self.game._running)

    def test_can_instantiate_game(self):
        self.assertIsInstance(self.game, Game)
        self.assertTrue(callable(self.game.start))
        self.assertIsInstance(self.game.director, Director)
        self.assertIsInstance(self.game.publisher, EventPublisher)
        self.assertIsInstance(self.game._running, bool)


if __name__ == '__main__':
    unittest.main()
