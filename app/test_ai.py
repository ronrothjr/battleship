import unittest
from ai import AI


class TestAI(unittest.TestCase):

    def test_can_instantiate_an_ai(self):
        self.ai = AI()
        self.assertIsInstance(self.ai, AI)


if __name__ == '__main__':
    unittest.main()
