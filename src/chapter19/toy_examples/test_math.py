import math
import unittest
import operator

class TestMath(unittest.TestCase):
    def testFloor(self):
        self.assertEqual(1, math.floor(1.01))
        self.assertEqual(0, math.floor(0.5))
        self.assertEqual(-1, math.floor(-0.5))
        self.assertEqual(-2, math.floor(-1.1))

    def testCeil(self):
        self.assertEqual(2, math.ceil(1.01))
        self.assertEqual(1, math.ceil(0.5))
        self.assertEqual(0, math.ceil(-0.5))
        self.assertEqual(-1, math.ceil(-1.1))

    def testDivision(self):
        self.assertRaises(ZeroDivisionError, operator.div, 1, 0)
        # The same assertion using a different idiom:
        self.assertRaises(ZeroDivisionError, lambda: 1 / 0)

    def testMultiplication(self):
        self.assertAlmostEqual(0.3, 0.1 * 3)

if __name__ == '__main__':
    unittest.main()
