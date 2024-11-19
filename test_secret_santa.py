import unittest
from secret_santa import secret_santa_shuffle, secret_santas_collide, parse_preseed

class TestSecretSanta(unittest.TestCase):

    def setUp(self):
        self.participants = {
            'Alice': 'alice@example.com',
            'Bob': 'bob@example.com',
            'Charlie': 'charlie@example.com',
            'David': 'david@example.com',
            'Eve': 'eve@example.com',
            'Frank': 'frank@example.com',
            'Grace': 'grace@example.com',
            'Heidi': 'heidi@example.com'
        }
        self.preseed_assignments = {
            'Alice': 'Bob'
        }
        self.past_years_assigns = [
            {
                'Alice': 'Charlie',
                'Bob': 'David',
                'Charlie': 'Eve',
                'David': 'Frank',
                'Eve': 'Grace',
                'Frank': 'Heidi',
                'Grace': 'Alice',
                'Heidi': 'Bob'
            },
            {
                'Alice': 'David',
                'Bob': 'Charlie',
                'Charlie': 'Frank',
                'David': 'Eve',
                'Eve': 'Heidi',
                'Frank': 'Grace',
                'Grace': 'Bob',
                'Heidi': 'Alice'
            },
            {
                'Alice': 'Frank',
                'Bob': 'Eve',
                'Charlie': 'Grace',
                'David': 'Heidi',
                'Eve': 'Alice',
                'Frank': 'Bob',
                'Grace': 'Charlie',
                'Heidi': 'David'
            }
        ]

    def get_valid_assignments(self):
        max_attempts = 1000
        for _ in range(max_attempts):
            try:
                assignments = secret_santa_shuffle(self.participants, self.preseed_assignments, debug=False)
                if not secret_santas_collide(assignments, self.past_years_assigns, debug=False):
                    return assignments
            except ValueError:
                continue
        raise ValueError("Could not find valid assignments after {} attempts".format(max_attempts))

    def test_secret_santa_shuffle(self):
        assignments = self.get_valid_assignments()
        self.assertEqual(assignments['Alice'], 'Bob')
        self.assertNotEqual(assignments['Bob'], 'Bob')
        self.assertNotEqual(assignments['Charlie'], 'Charlie')
        self.assertNotEqual(assignments['David'], 'David')
        self.assertNotEqual(assignments['Eve'], 'Eve')
        self.assertNotEqual(assignments['Frank'], 'Frank')
        self.assertNotEqual(assignments['Grace'], 'Grace')
        self.assertNotEqual(assignments['Heidi'], 'Heidi')

    def test_secret_santas_collide(self):
        assignments = self.get_valid_assignments()
        self.assertFalse(secret_santas_collide(assignments, self.past_years_assigns, debug=False))

    def test_parse_preseed(self):
        preseed_str = 'Alice:Bob,Charlie:David'
        preseed_assignments = parse_preseed(preseed_str)
        self.assertEqual(preseed_assignments['Alice'], 'Bob')
        self.assertEqual(preseed_assignments['Charlie'], 'David')

    def test_list_is_complete(self):
        assignments = self.get_valid_assignments()
        self.assertEqual(len(assignments), len(self.participants))
        for name in self.participants.keys():
            self.assertIn(name, assignments)
            self.assertIn(assignments[name], self.participants.keys())

if __name__ == '__main__':
    unittest.main()