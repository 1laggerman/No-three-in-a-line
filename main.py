import random
from timeit import default_timer as timer
from package import Point, Grid as Point, Grid

def __main__():
    grid = Grid(n=10, d=2)
    grid.add_point(Point(0, 0))
    grid.draw_grid()
    


def order_solutions(n):
    grid = Grid(n=n, d=2)

    grid.find_max_solutions_2D()

    print('2D solutions:')
    for index, solution in grid.solutions:
        print(index, solution)
    
    start = timer()
    solutions = grid.order_2D_solutions(1, method='All')
    time = timer() - start
    print('time to find order: ', time)
    grid.d = 3
    print(solutions)
    
if __name__ == '__main__':
    __main__()
