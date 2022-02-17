import unittest
from setting import Setting
from mock_pygame import MockPygame


class TestSetting(unittest.TestCase):

    def setUp(self) -> None:
        self.scene = Setting(MockPygame(), 'splash', {'title': 'Splash', 'bg': 'battleship.jpeg', 'size': {'width': 755, 'height': 755}})
    
    def test_can_instantiate_a_scene(self):
        self.assertIsInstance(self.scene, Setting)
        self.assertIsInstance(self.scene.name, str)
        self.assertIsInstance(self.scene.title, str)
        self.assertIsInstance(self.scene.size, tuple)
        self.assertIsInstance(self.scene.bg, str)
        self.assertTrue(callable(self.scene.on_init))

    def test_can_init_a_scene(self):
        self.scene.on_init()
        self.assertIsNotNone(self.scene.screen)
        self.assertIsNotNone(self.scene.background)




if __name__ == '__main__':
    unittest.main()