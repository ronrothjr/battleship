import unittest
from files_mock import FilesMock
from test_files import BaseFileTestCases

class TestFilesMock(BaseFileTestCases.BaseTestFiles):

    def setUp(self):
        self.files = FilesMock()
        self.files.write_file('test_data', 'John,1234')

if __name__ == '__main__':
    unittest.main() 
