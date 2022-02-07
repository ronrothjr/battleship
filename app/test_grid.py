import copy, unittest
from coordinates import Coordinates
from grid import Grid
from ship import Ship
from shot import Shot


class TestGrid(unittest.TestCase):

    def setUp(self) -> None:
        self.grid = Grid()

    def test_can_instantiate_a_grid(self):
        self.assertIsInstance(Grid.x, list)
        self.assertIsInstance(Grid.y, list)
        self.assertTrue(callable(Grid.get_location_coordinates))
        self.assertIsInstance(self.grid, Grid)
        self.assertIsInstance(self.grid.ships, list)
        self.assertIsInstance(self.grid.shots, list)
        self.assertEqual(self.grid.add_ship.__name__, 'add_ship')
        self.assertTrue(callable(self.grid.add_ship))
        self.assertEqual(self.grid.mark_shot.__name__, 'mark_shot') 
        self.assertTrue(callable(self.grid.mark_shot))

    def test_grid_can_add_ship(self):
        ship1 = Ship('Destroyer')
        ship1.set_location([Coordinates({'x': 'E', 'y': '5'}), Coordinates({'x': 'E', 'y': '6'})])
        added = self.grid.add_ship(ship1)
        self.assertTrue(added)

    def test_grid_cannot_add_ship_with_same_coordinates_or_model(self):
        ship1 = Ship('Destroyer')
        ship1.set_location([Coordinates({'x': 'E', 'y': '5'}), Coordinates({'x': 'E', 'y': '6'})])
        added = self.grid.add_ship(ship1)
        ship2 = Ship('Cruiser')
        ship2.set_location([Coordinates({'x': 'E', 'y': '5'}), Coordinates({'x': 'D', 'y': '5'}), Coordinates({'x': 'C', 'y': '5'})])
        added = self.grid.add_ship(ship2)
        self.assertFalse(added)
        ship2 = Ship('Destroyer')
        ship2.set_location([Coordinates({'x': 'B', 'y': '5'}), Coordinates({'x': 'C', 'y': '5'})])
        added = self.grid.add_ship(ship2)
        self.assertFalse(added)
        self.assertEqual(len(self.grid.ships), 1)

    def test_grid_can_mark_shot_and_set_the_shot_as_a_hit(self):
        ship1 = Ship('Destroyer')
        ship1.set_location([Coordinates({'x': 'E', 'y': '5'}), Coordinates({'x': 'E', 'y': '6'})])
        added = self.grid.add_ship(ship1)
        shot = Shot(Coordinates({'x': 'E', 'y': '5'}))
        self.grid.mark_shot(shot)
        self.assertEqual(len(self.grid.shots), 1)
        self.assertTrue(shot.hit)

    def test_grid_cannot_mark_shot_that_was_already_marked(self):
        ship1 = Ship('Destroyer')
        ship1.set_location([Coordinates({'x': 'E', 'y': '5'}), Coordinates({'x': 'E', 'y': '6'})])
        added = self.grid.add_ship(ship1)
        shot1 = Shot(Coordinates({'x': 'E', 'y': '5'}))
        shot_taken = self.grid.mark_shot(shot1)
        self.assertTrue(shot_taken)
        self.assertEqual(len(self.grid.shots), 1)
        shot2 = Shot(Coordinates({'x': 'E', 'y': '5'}))
        shot_taken = self.grid.mark_shot(shot2)
        self.assertFalse(shot_taken)
        self.assertEqual(len(self.grid.shots), 1)


if __name__ == '__main__':
    unittest.main()
