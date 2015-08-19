"""
    KD Factory implementation.

    Author: George Heineman
"""
import unittest

from kd2 import KDTree
from kd_factory import generate, generateSubTree
from region import Region, X, Y
import random

class TestKDTree(unittest.TestCase):

    def test_three(self):
        pts = [(20, 10), (90, 50), (60, 80)]

        tree = generate(pts)
        self.assertEqual(60, tree.root.point[X])

        # on X-coordinate
        self.assertEqual(20, tree.root.below.point[X])
        self.assertEqual(90, tree.root.above.point[X])

        # regions
        self.assertEqual(60, tree.root.below.region.x_max)

    def test_five(self):
        pts = [(20, 10), (90, 50), (60, 80), (70, 30), (40, 100)]

        tree = generate(pts)
        self.assertEqual(60, tree.root.point[X])

        # on X-coordinate
        self.assertEqual(20, tree.root.below.point[X])
        self.assertEqual(70, tree.root.above.point[X])    
        
if __name__ == '__main__':
    unittest.main()
    
