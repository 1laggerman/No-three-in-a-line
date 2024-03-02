import unittest

from package.PointG import PointG as Point
from package.GridG import GridG as Grid

from package.validPointsStruct import validPoints

# from package import Point
# from package import Grid


class TestStringMethods(unittest.TestCase):

    def test_point_Stringify(self):
        p1 = Point(0, 1, 1)
        self.assertEqual(p1.__str__(), '(0, 1, 1)')
        
        p2 = Point(0, 1, 2, 3, 4, 5, 4, 3, 2, 1)
        self.assertEqual(p2.__str__(), '(0, 1, 2, 3, 4, 5, 4, 3, 2, 1)')
        
    def test_grid_Stringify(self):
        g1 = Grid(d=4, n=4)
        g1.add_point(Point(0, 0, 0, 0))
        self.assertEqual(g1.__str__(), '[(0, 0, 0, 0)]', g1.__str__())
        
        g1.add_points([Point(0, 0, 0, 1), Point(0, 0, 3, 1), Point(1, 1, 3, 3)])
        self.assertEqual(g1.__str__(), '[(0, 0, 0, 0), (0, 0, 0, 1), (0, 0, 3, 1), (1, 1, 3, 3)]')
        
    def test_collinear(self):
        p1 = Point(0, 0, 0)
        
        p2 = Point(1, 1, 1)
        p3 = Point(3, 3, 3)
        
        self.assertTrue(p1.onTheSameLine(p2, p3))
        self.assertTrue(p2.onTheSameLine(p1, p3))
        self.assertTrue(p3.onTheSameLine(p2, p1))
        
        
        p2 = Point(0, 0, 1)
        p3 = Point(0, 0, 2)
        
        self.assertTrue(p1.onTheSameLine(p2, p3))
        self.assertTrue(p2.onTheSameLine(p1, p3))
        self.assertTrue(p3.onTheSameLine(p2, p1))
        
        p4 = Point(0, 1, 1)
        p5 = Point(1, 0, 0)
        
        self.assertFalse(p4.onTheSameLine(p1, p2))
        self.assertFalse(p4.onTheSameLine(p1, p3))
        self.assertFalse(p5.onTheSameLine(p2, p3))
        
    def test_Fastcollinear(self):
        p1 = Point(0, 0, 0)
        
        p2 = Point(1, 1, 1)
        p3 = Point(3, 3, 3)
        
        self.assertTrue(p1.onTheSameLineFast(p2, p3))
        self.assertTrue(p2.onTheSameLineFast(p1, p3))
        self.assertTrue(p3.onTheSameLineFast(p2, p1))
        
        
        p2 = Point(0, 0, 1)
        p3 = Point(0, 0, 2)
        
        self.assertTrue(p1.onTheSameLineFast(p2, p3))
        self.assertTrue(p2.onTheSameLineFast(p1, p3))
        self.assertTrue(p3.onTheSameLineFast(p2, p1))
        
        p4 = Point(0, 1, 1)
        p5 = Point(1, 0, 0)
        
        self.assertFalse(p4.onTheSameLineFast(p1, p2))
        self.assertFalse(p4.onTheSameLineFast(p1, p3))
        self.assertFalse(p5.onTheSameLineFast(p2, p3))
        
    def test_comparison(self):
        
        p1 = Point(0, 0, 0)
        p2 = Point(0, 0, 1)
        p3 = Point(1, 1, 0)
        p4 = Point(0, 1, 1)
        
        self.assertTrue(p1 < p2)
        self.assertTrue(p2 > p1)
        self.assertTrue(p3 < p2)
        self.assertTrue(p4 > p2)
        self.assertTrue(p3 < p4)
        
    def test_hash(self):
        s1 = set([Point(0, 1, 1, n=3), Point(1, 0, 0, n=3), Point(1, 1, 0, n=3), Point(2, 1, 2)])
        s2 = set([Point(1, 1, 0, n=3), Point(0, 0, 0, n=3), Point(2, 2, 1, n=3)])
        s3 = set([x for x in s1 if x not in s2])
        s_res = set([Point(0, 1, 1, n=3), Point(1, 0, 0, n=3), Point(2, 1, 2, n=3)])
        self.assertEqual(s3, s_res)        
        
    def test_GetAllValidPoints(self):
        g = Grid(2, 3)
        VP = g.getAllValidPoints()
        validPoints = set([Point(0, 0, 0, n=2), Point(1, 0, 0, n=2), Point(0, 1, 0, n=2), Point(1, 1, 0, n=2), Point(0, 0, 1, n=2), Point(1, 0, 1, n=2), Point(0, 1, 1, n=2), Point(1, 1, 1, n=2)])
        self.assertEqual(validPoints, VP)
    
    
    def test_validPointStruct(self):
        g = Grid(2, 3)
        VP = validPoints(g.getAllValidPoints(), 2, 3)
        
        VP.remove(Point(0, 0))
        VP.remove(Point(2, 2))
        VP.remove(Point(1, 1))
        # [(1, 2), (1, 0), (2, 0), (0, 1), (0, 2), (2, 1)]
        # [[-1  3  4]
        #  [ 1 -1  0]
        #  [ 2  5 -1]]
        valid_points = validPoints([])
        
    
    # def test_removeInValidPoints(self):
    #     g = Grid(3, 2)
    #     vp = g.getAllValidPoints()
    #     added = [Point(0, 0), Point(0, 1), Point(1, 0)]
    #     new_vp = g.removeInValidPoints(added, vp)
    #     valid_points = [Point(1, 1), Point(2, 1), Point(1, 2), Point(2, 2)]
    #     self.assertEqual(new_vp, valid_points)
        

if __name__ == '__main__':
    unittest.main()