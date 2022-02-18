import unittest
from mock_pygame import MockPygame
from director import Director
from event_publisher import EventPublisher
from scenes.settings import settings
from setting import Setting


class TestDirector(unittest.TestCase):

    def setUp(self) -> None:
        self.director = Director(MockPygame())

    def test_can_instantiate_director(self):
        self.assertIsInstance(self.director, Director)
        self.assertIsInstance(self.director.publisher, EventPublisher)
        self.assertTrue(callable(self.director.set_scenes))
        self.assertTrue(callable(self.director.call))

    def test_can_set_scene(self):
        self.director.set_scenes(settings)
        self.assertTrue(len(self.director.scenes.keys()), 1)

    def test_can_call_and_cut_a_scene(self):
        self.director.set_scenes(settings)
        self.director.call('splash')
        self.assertIsInstance(self.director.current_scene, Setting)
        self.director.call('splash')
        self.assertIsInstance(self.director.current_scene, Setting)


if __name__ == '__main__':
    unittest.main()