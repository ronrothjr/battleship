import unittest
from coordinates import Coordinates
from shot import Shot


class TestShot(unittest.TestCase):
    def test_can_instantiate_a_shot(self):
        coordinates = Coordinates({'x': 'E', 'y': 5})
        self.shot = Shot(coordinates)
        self.assertIsInstance(self.shot, Shot)
        self.assertIsInstance(self.shot.hit, bool)
        self.assertIsInstance(self.shot.coordinates, Coordinates)


if __name__ == '__main__':
    unittest.main()
