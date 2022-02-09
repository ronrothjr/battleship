import unittest
from data import Data
from files_mock import FilesMock

class TestData(unittest.TestCase):

    def setUp(self):
        self.data = Data(FilesMock())

    def test_data_init_creates_empty_collections(self):
        self.assertEqual(self.data.collections, {})
        self.assertEqual(self.data.get_object_dict.__name__, 'get_object_dict') 
        self.assertTrue(callable(self.data.get_object_dict))

    def test_decode_records_should_return_empty_array_if_none(self):
        records = self.data.decode_records(None)
        self.assertEqual(records, [])

    def test_decode_records_should_return_list_if_not_empty(self):
        records = self.data.decode_records('[{"username":"John","password":"1234"}]')
        self.assertEqual(records, [{"username":"John","password":"1234"}])

    def test_encode_records_should_return_none_if_empty_array(self):
        file_str = self.data.encode_records([])
        self.assertEqual(file_str, '[]')

    def test_save_records_from_list(self):
        file_size = self.data.save_records('test_data', [{"username":"John","password":"1234"}, {"username":"Jane","password":"4321"}])
        self.assertEqual(file_size, 84)

    def test_encode_records_should_retutn_str_if_list_has_data(self):
        file_str = self.data.encode_records([{"username":"John","password":"1234"}, {"username":"Jane","password":"4321"}])
        self.assertEqual(file_str, '[{"username": "John", "password": "1234"}, {"username": "Jane", "password": "4321"}]')

    def test_load_records_returns_empty_list_if_collection_does_not_exist(self):
        test_data2 = self.data.load_records('test_data2')
        self.assertEqual(test_data2, [])

if __name__ == '__main__':
    unittest.main() 