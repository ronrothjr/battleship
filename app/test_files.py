import unittest
from unittest.mock import patch
from files import Files

class BaseFileTestCases:

    class BaseTestFiles(unittest.TestCase):

        def setUp(self):
            self.files = Files()
            self.files.write_file('test_data', 'John,1234')

        def tearDown(self):
            self.files.remove_path('test_path')
            self.files.remove_file('test_file')
            self.files.remove_file('test_data')

        def test_if_init_sets_the_current_directory_path(self):
            self.assertIsNotNone(self.files.local_path)

        def test_if_init_determines_path_separator(self):
            self.assertIn(self.files.path_separator, ['\\', '/'])

        def test_if_path_exists_returns_boolean_if_exists(self):
            with patch.object(self.files, 'path_exists', wraps=self.files.path_exists) as spy_path_exists:
                path_exists = spy_path_exists('test_path')
                spy_path_exists.assert_called_once_with('test_path')
                self.assertFalse(path_exists)
                path_exists = spy_path_exists(self.files.local_path)

        def test_create_path_returns_true_if_path_is_created(self):
            with patch.object(self.files, 'create_path', wraps=self.files.create_path) as spy_create_path:
                path_created = spy_create_path('test_path')
                spy_create_path.assert_called_once_with('test_path')
                self.assertTrue(path_created)
                path_created = spy_create_path('test_path')
                self.assertFalse(path_created)
            path_exists = self.files.path_exists('test_path')
            self.assertEqual(path_exists, True)

        def test_remove_path_returns_true_if_path_is_removed(self):
            with patch.object(self.files, 'remove_path', wraps=self.files.remove_path) as spy_remove_path:
                self.files.create_path('test_path')
                path_removed = spy_remove_path('test_path')
                spy_remove_path.assert_called_once_with('test_path')
                self.assertTrue(path_removed)
                path_removed = spy_remove_path('test_path')
                self.assertFalse(path_removed)
            path_exists = self.files.path_exists('test_path')
            self.assertFalse(path_exists)

        def test_write_file_returns_file_size_if_written(self):
            with patch.object(self.files, 'write_file', wraps=self.files.write_file) as spy_write_file:
                file_size = spy_write_file('test_file', 'test file data')
                spy_write_file.assert_called_once_with('test_file', 'test file data')
                self.assertEqual(file_size, 14)
            path_exists = self.files.path_exists('test_file.txt')
            self.assertTrue(path_exists)

        def test_remove_file_returns_false_if_does_not_exist(self):
            with patch.object(self.files, 'remove_file', wraps=self.files.remove_file) as spy_remove_file:
                removed = spy_remove_file('test_file')
                spy_remove_file.assert_called_once_with('test_file')
                self.assertFalse(removed)

        def test_remove_file_returns_true_if_exists(self):
            self.save_test_file()
            with patch.object(self.files, 'remove_file', wraps=self.files.remove_file) as spy_remove_file:
                removed = spy_remove_file('test_file')
                spy_remove_file.assert_called_once_with('test_file')
                self.assertTrue(removed)
                removed = spy_remove_file('test_file')
                self.assertFalse(removed)

        def test_read_file_returns_none_if_file_does_not_exist(self):
            with patch.object(self.files, 'read_file', wraps=self.files.read_file) as spy_read_file:
                file_str = spy_read_file('test_file')
                spy_read_file.assert_called_once_with('test_file')
                self.assertIsNone(file_str)

        def test_read_file_returns_str_contents_if_exists(self):
            with patch.object(self.files, 'read_file', wraps=self.files.read_file) as spy_read_file:
                file_str = spy_read_file('test_data')
                spy_read_file.assert_called_once_with('test_data')
                self.assertEqual(file_str, 'John,1234')
                file_str = spy_read_file('test_data')
                self.assertEqual(spy_read_file.call_count, 2)
                self.assertEqual(file_str, 'John,1234')

        def save_test_file(self) -> int:
            file_size = self.files.write_file('test_file', 'test file data')
            return file_size

class TestFiles(BaseFileTestCases.BaseTestFiles):
    pass

if __name__ == '__main__':
    unittest.main() 
