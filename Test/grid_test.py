import unittest

from package.Point import Point as Point
from package.Grid import Grid as Grid

from package.GridPointsStruct import GridPoints

class TestGrid(unittest.TestCase):
    
    def test_grid_Stringify(self):
        g1 = Grid(d=4, n=4)
        g1.add_point(Point(0, 0, 0, 0))
        self.assertEqual(g1.__str__(), '[(0, 0, 0, 0)]', g1.__str__())
        
        g1.add_points([Point(0, 0, 0, 1), Point(0, 0, 3, 1), Point(1, 1, 3, 3)])
        self.assertEqual(g1.__str__(), '[(0, 0, 0, 0), (0, 0, 0, 1), (0, 0, 3, 1), (1, 1, 3, 3)]')
        
    # def test_removeInValidPoints(self):
    #     g = Grid(3, 2)
    #     vp = g.getAllValidPoints()
    #     added = [Point(0, 0), Point(0, 1), Point(1, 0)]
    #     new_vp = g.removeInValidPoints(added, vp)
    #     valid_points = [Point(1, 1), Point(2, 1), Point(1, 2), Point(2, 2)]
    #     self.assertEqual(new_vp, valid_points) 