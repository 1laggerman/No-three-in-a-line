import unittest

from package.Point import Point as Point
from package.Grid import Grid as Grid
import numpy as np

from package.GridPointsStruct import GridPoints

class TestGridPoints(unittest.TestCase):
    
    def test_str(self):
        gp = GridPoints(n=3, d=2, k_in_line=2)
        chosen = []
        valid = [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)]
        idx = np.array([[-1, -4, -7], [-2, -5, -8], [-3, -6, -9]])
        collision = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        gp_str = f'chosen: {chosen}\nvalid: {valid}\nidx_mat: \n{idx}\ncollisions: \n{collision}'
        self.assertEqual(gp.__str__(), gp_str)
        
    def test_add(self):
        gp = GridPoints(n=3, d=2, k_in_line=2)
        gp.add(Point(0, 0, n=3))
        
        gp_add = GridPoints(n=3, d=2, k_in_line=2)
        gp_add.chosen.append(Point(0, 0, n=3))
        gp_add.valid
        self.assertTrue()
        