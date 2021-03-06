import io, unittest
from unittest.mock import patch
from coordinates import Coordinates
from session import Session
from ai import AI
from player import Player
from shot import Shot


class TestAI(unittest.TestCase):

    def setUp(self) -> None:
        self.ai = AI()

    def test_can_instantiate_an_ai(self):
        self.assertIsInstance(self.ai, AI)
        self.assertEqual(self.ai.place_ship.__name__, 'place_ship') 
        self.assertTrue(callable(self.ai.place_ship))
        self.assertEqual(self.ai.get_shot.__name__, 'get_shot') 
        self.assertTrue(callable(self.ai.get_shot))
        self.assertEqual(self.ai.get_location_of_damaged_ship.__name__, 'get_location_of_damaged_ship') 
        self.assertTrue(callable(self.ai.get_location_of_damaged_ship))
        self.assertEqual(self.ai.get_shot_near_damaged_ship.__name__, 'get_shot_near_damaged_ship') 
        self.assertTrue(callable(self.ai.get_shot_near_damaged_ship))
        self.assertEqual(self.ai.add_nearby_coordinates.__name__, 'add_nearby_coordinates') 
        self.assertTrue(callable(self.ai.add_nearby_coordinates))

    def test_ai_can_return_a_random_set_of_x_y_coordinates_excluding_previous_shots(self):
        x_y = self.ai.get_shot(Player(), Player())
        self.assertIsInstance(x_y, dict)
        self.assertIsInstance(x_y['x'], str)
        self.assertIsInstance(x_y['y'], str)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_ai_can_get_shots_on_ships_not_yet_sunk(self, mock_stdout):
        session = Session()
        session.players = [Player(is_ai=True), Player(is_ai=True)]
        p1 = session.players[0]
        p2 = session.players[1]
        session.place_ships(p1)
        session.place_ships(p2)
        coordinates = p2.grid.ships[0].location[0]
        shot = Shot(coordinates=coordinates)
        p2.take_a_shot(shot)
        p1.grid.add_shot(shot)
        all_shots_taken = p1.grid.get_all_shots_taken()
        damaged_ship_coordinates = self.ai.get_location_of_damaged_ship(p2, all_shots_taken)
        self.assertEqual(shot.coordinates, damaged_ship_coordinates[0])
        coordinates_near_damaged_ship = self.ai.get_shot_near_damaged_ship(all_shots_taken, damaged_ship_coordinates)
        self.assertIsInstance(coordinates_near_damaged_ship, Coordinates)


if __name__ == '__main__':
    unittest.main()
