import unittest
from secret_santa import secret_santa_shuffle, secret_santas_collide, parse_preseed

class TestSecretSanta(unittest.TestCase):

    def setUp(self):
        self.participants = {
            'Alice': 'alice@example.com',
            'Bob': 'bob@example.com',
            'Charlie': 'charlie@example.com',
            'David': 'david@example.com'
        }
        self.preseed_assignments = {
            'Alice': 'Bob'
        }
        self.last_year_assigns = {
            'Alice': 'Charlie',
            'Bob': 'David',
            'Charlie': 'Alice',
            'David': 'Bob'
        }
        self.other_year_assigns = {
            'Alice': 'David',
            'Bob': 'Charlie',
            'Charlie': 'Bob',
            'David': 'Alice'
        }

    def test_secret_santa_shuffle(self):
        assignments = secret_santa_shuffle(self.participants, self.preseed_assignments, debug=True)
        self.assertEqual(assignments['Alice'], 'Bob')
        self.assertNotEqual(assignments['Bob'], 'Bob')
        self.assertNotEqual(assignments['Charlie'], 'Charlie')
        self.assertNotEqual(assignments['David'], 'David')

    def test_secret_santas_collide(self):
        assignments = secret_santa_shuffle(self.participants, self.preseed_assignments, debug=True)
        self.assertFalse(secret_santas_collide(assignments, self.last_year_assigns, self.other_year_assigns, debug=True))

    def test_parse_preseed(self):
        preseed_str = 'Alice:Bob,Charlie:David'
        preseed_assignments = parse_preseed(preseed_str)
        self.assertEqual(preseed_assignments['Alice'], 'Bob')
        self.assertEqual(preseed_assignments['Charlie'], 'David')

    def test_list_is_complete(self):
        assignments = secret_santa_shuffle(self.participants, self.preseed_assignments, debug=True)
        self.assertEqual(len(assignments), len(self.participants))
        for name in self.participants.keys():
            self.assertIn(name, assignments)
            self.assertIn(assignments[name], self.participants.keys())

if __name__ == '__main__':
    unittest.main()