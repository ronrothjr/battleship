import pygame, threading, unittest
from pygame.locals import *
from game import Game
from mock_pygame import MockPygame, MockDisplaySurface, MockImageSurface

        
class TestGame(unittest.TestCase):

    def setUp(self) -> None:
        self.game = Game(MockPygame())
        self.assertTrue(self.game._running)
        threading.Timer(0.1, self.game.pygame.event.post, [self.game.pygame.event.Event(QUIT)]).start()
        self.game.start()

    def tearDown(self) -> None:
        self.assertFalse(self.game._running)

    def test_can_instantiate_game(self):
        self.assertIsInstance(self.game, Game)
        self.assertTrue(callable(self.game.start))
        self.assertIsInstance(self.game._running, bool)
        self.assertIsInstance(self.game.size, tuple)
        self.assertIsInstance(self.game.width, int)
        self.assertIsInstance(self.game.height, int)


if __name__ == '__main__':
    unittest.main()
