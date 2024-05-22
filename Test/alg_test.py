
import unittest
import random

from package.Point import Point as Point
from package.Grid import Grid as Grid

from package.GridPointsStruct import GridPoints

class TestGrid(unittest.TestCase):
    
    def test_random_greedy(self):
        random.seed(a=0)
        n = 3
        d = 2
        g = Grid(n=n, d=d)
        points, num = g.random_greedy()
        print(points, ', ', num)
        assert num == 5
        assert points == GridPoints([Point(0, 2, n=n), Point(2, 2, n=n), Point(0, 0, n=n), Point(1, 0, n=n), Point(2, 1, n=n)], n=n, d=d)