import unittest
from fuzzy import match_fuzzy

class TestFuzzy(unittest.TestCase):

    def setUp(self):
        self.words = [
            'chubby Captain',
            'shiny shell',
            'shipwreck/trove/fortune/risk',
            'abc-cba.123abc',
            '#..%@clipclap',
            'disk/is/Full/Sorry/dude',
            'sorry fuzzy JAccuzi',
            ]

        self.str_to_match = [
            ('cuca', ['chubby Captain']),
            ('cap', ['chubby Captain', '#..%@clipclap']),
            ('fsd', ['disk/is/Full/Sorry/dude']),
            ('c3c', ['abc-cba.123abc']),
            ('neri', ['shipwreck/trove/fortune/risk']),
        ]

    def test_basic(self):
        for _str, match in self.str_to_match:
            self.assertListEqual(match_fuzzy(_str, self.words), match)

if __name__ == '__main__':
    unittest.main()
