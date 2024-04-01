import unittest

from package.Point import Point as Point
from package.Grid import Grid as Grid

from package.GridPointsStruct import GridPoints

class TestGridPoints(unittest.TestCase):
    
    def test_str(self):
        gp = GridPoints(n=3, d=3, k_in_line=2)
        gp_str = "[]"
        self.assertEqual(gp.__str__(), gp_str)