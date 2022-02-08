import unittest
from coordinates import Coordinates
from ship import Ship


class TestShot(unittest.TestCase):

    def setUp(self) -> None:
        self.ship = Ship('Destroyer')

    def test_can_instantiate_a_shot(self):
        self.assertIsInstance(self.ship, Ship)
        self.assertIsInstance(self.ship.location, list)
        self.assertIsInstance(self.ship.model, str)
        self.assertIsInstance(self.ship.size, int)
        self.assertEqual(self.ship.set_location.__name__, 'set_location') 
        self.assertTrue(callable(self.ship.set_location))
        self.assertEqual(self.ship.is_sunk.__name__, 'is_sunk') 
        self.assertTrue(callable(self.ship.is_sunk))

    def test_can_set_ship_location(self):
        location = [Coordinates({'x': 'E', 'y': '5'}), Coordinates({'x': 'E', 'y': '6'})]
        location_set = self.ship.set_location(location)
        self.assertTrue(location_set)
        self.assertTrue(self.ship.location, location)

    def test_cannot_set_ship_location_that_do_not_match_size(self):
        location = [Coordinates({'x': 'E', 'y': '5'}), Coordinates({'x': 'E', 'y': '6'}), Coordinates({'x': 'E', 'y': '7'})]
        location_set = self.ship.set_location(location)
        self.assertFalse(location_set)

    def test_ship_can_tell_whether_it_is_sunk(self):
        location = [Coordinates({'x': 'E', 'y': '5'}), Coordinates({'x': 'E', 'y': '6'})]
        self.ship.set_location(location)
        self.ship.location[0].hit = True
        self.ship.location[1].hit = True
        is_sunk = self.ship.is_sunk()
        self.assertTrue(is_sunk)

    def test_ship_can_tell_whether_it_is_not_sunk(self):
        location = [Coordinates({'x': 'E', 'y': '5'}), Coordinates({'x': 'E', 'y': '6'})]
        self.ship.set_location(location)
        self.ship.location[0].hit = True
        is_sunk = self.ship.is_sunk()
        self.assertFalse(is_sunk)



if __name__ == '__main__':
    unittest.main()
