import unittest
from coordinates import Coordinates


class TestCoordinates(unittest.TestCase):
    def test_can_instantiate_a_shot(self):
        self.coordinates = Coordinates({'x': 'E', 'y': 5})
        self.assertIsInstance(self.coordinates, Coordinates)
        self.assertIsInstance(self.coordinates.x, str)
        self.assertIsInstance(self.coordinates.y, int)
        self.assertIsInstance(self.coordinates.hit, bool)
        self.assertIsInstance(self.coordinates.model, str)


if __name__ == '__main__':
    unittest.main()