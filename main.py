import random
from timeit import default_timer as timer
from package import Point, Grid

def __main__():
    n = 6
    grid = Grid(n=n, d=2)

    grid.find_max_solutions_2D()

    print('2D solutions:')
    for index, solution in grid.solutions:
        print(index, solution)
    
    start = timer()
    solutions = grid.order_2D_solutions(1, method='All')
    time = timer() - start
    print(time)
    grid.d = 3
    print(solutions)
    # points: list[Point] = list()
    # index = 0
    # for s in solutions[0][0]:
    #     bol = grid.solutions[s][1].copy()
    #     for i in range(bol.__len__()):
    #         bol[i].z = index
    #     points.extend(copy.deepcopy(bol))
    #     index = index + 1
        
    # print(points)
    # grid.points = points
    # grid.draw_grid()
    
__main__()
