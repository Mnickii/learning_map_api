import unittest
from dummy import multiplyDigits


class DummyTest(unittest.TestCase):
    """Write Dummy Test for Learning Map API"""

    def testDummyFunction(self):
        result = multiplyDigits(2, 3)
        self.assertEqual(result, 6)


if __name__ == "__main__":
    unittest.main()
