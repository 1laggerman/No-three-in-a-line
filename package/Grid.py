import matplotlib.pyplot as plt
import numpy as np
import itertools as it
import copy
from .Point import Point
import functools

# from numba import jit, cuda
import tensorflow as tf
import multiprocessing

class Grid:
    points = list()
    n = 1
    d = 2
    solutions: list[tuple[int, list[Point]]]
    
    def __init__(self, n: int = 3, d: int = 2):
        self.n = n
        self.d = d
        
    def add_point(self, p: Point):
        self.points.append(p)
        
    def add_points(self, points_arr: list):
        for point in points_arr:
            self.points.append(point)
            
    def is_solution(self, points: list[Point]):
        points.extend(self.points)
        
        for point1, point2, point3 in it.combinations(points, 3):
            if point1.onTheSameLine(point2, point3):
                return False
        return True
    
    def getAllValidPoints(self, d: int = 2, z_layer: int = 0, chosen: list = list()):
        chosen.extend(self.points)
        ValidPoints: list[Point] = list()
        
        for z in range(self.n):
            for x in range(self.n):
                for y in range(self.n):
                    if d == 2:
                        if len(self.points) > 0:
                            z = chosen[0].z
                        else:
                            z = z_layer
                            
                    thisPoint = Point(x, y, z)
                    
                    if len(chosen) == 0:
                        ValidPoints.append(thisPoint)
                    elif len(chosen) == 1:
                        if thisPoint != chosen[0]:
                            ValidPoints.append(thisPoint)
                    else:
                        pointValid = True
                        for point1, point2 in it.combinations(chosen, 2):
                            if thisPoint.onTheSameLine(point1, point2):
                                pointValid = False
                        if pointValid:
                            ValidPoints.append(thisPoint)
                        
            if d == 2:
                break
                                
        return ValidPoints
    
    # TODO: integrate this generalized function version in the existing algorithms
    def removeInValidPoints(self, chosen_points: list[Point], added_points: list[Point], valid_points: list[Point]):
        for chosen_point in chosen_points:
            for added_point in added_points:
                valid_index = 0
                while valid_index < valid_points.__len__():
                    if valid_points[valid_index].onTheSameLine(chosen_point, added_point):
                        valid_points.pop(valid_index)
                        valid_index = valid_index - 1
                    valid_index = valid_index + 1
                        
        return valid_points
    
    def removeInValidPoints_2n_new(self, chosen_points: list[Point], added_points: list[Point], z_layer: int, valid_points: list[Point], isSolution: bool = True):
        while valid_points[0].z == z_layer:
            valid_points.pop(0)
            
        for chosen_point in chosen_points:
            for added_point in added_points:
                valid_index = 0
                while valid_index < valid_points.__len__():
                    if valid_points[valid_index].onTheSameLine(chosen_point, added_point):
                        valid_points.pop(valid_index)
                        valid_index = valid_index - 1
                    valid_index = valid_index + 1
                        
        return valid_points
            
    def removeInValidPoints_2_new(self, added1: Point, added2: Point, valid: list, chosen: list = list()):
        
        if added1.x == added2.x and added1.z == added2.z:
            for i in range(self.n):
                try:
                    valid.remove(Point(added1.x, i, added1.z))
                except:
                    pass
                    
         
        for point1 in chosen:
            if point1 != added1 and point1 != added2:
                i = 0
                while i < len(valid):
                    if added1.onTheSameLine(point1, valid[i]) or added2.onTheSameLine(point1, valid[i]):
                        valid.remove(valid[i])
                        i = i - 1
                    i = i + 1
        return valid
    
    def removeInValidPoints_1_new(self, added1: Point, valid: list, chosen: list = list()):
        for point1 in chosen:
            if point1 != added1:
                i = 0
                while i < len(valid):
                    if added1.onTheSameLine(point1, valid[i]):
                        valid.remove(valid[i])
                        i = i - 1
                    i = i + 1
        return valid
    
    
    def process_solution(self, solution, method, valid_points):
        xy_mat = np.zeros((self.n, self.n))
        chosen = [point for point in solution[1]]
        for point in chosen:
            xy_mat[point.x, point.y] = 1

        if method == 'valid_points':
            return self.choose_solution_recursive(
                [solution[0]], [index for index, _ in self.solutions], chosen, valid_points, xy_mat, (False, True)
            )
        elif method == 'valid_matrix':
            return self.choose_solution_recursive([solution[0]], [index for index, _ in self.solutions], chosen, valid_points, xy_mat, (True, False))
        elif method == 'All':
            return self.choose_solution_recursive([solution[0]], [index for index, _ in self.solutions], chosen, valid_points, xy_mat, (True, True))
    
    # 3D algorithms:
    def order_2D_solutions(self, proba: float = 1, method='valid_points', cpu_process=(multiprocessing.cpu_count()/2) - 2):
        if __name__ == '__main__' or __name__ == 'package.Grid':
            max_result = (list(), 0)
            valid_points = self.getAllValidPoints(d=3)
            while valid_points[0].z == 0:
                valid_points.pop(0)

            partial_process_solution = functools.partial(self.process_solution, method=method, valid_points=valid_points)

            cpu_process = int(min(cpu_process, multiprocessing.cpu_count() / 2))
            print(f'Running as {cpu_process} processes on {int(multiprocessing.cpu_count()/2)} cores')

            # TODO - HOME: test if tensorflow recognizes and uses GPU to calculate
            # Check if GPU is available
            if tf.config.list_physical_devices('GPU'):
                gpus = tf.config.experimental.list_physical_devices('GPU')
                if gpus and len(gpus) > 1:
                    strategy = tf.distribute.MirroredStrategy(devices=['/GPU:0', '/GPU:1'])  # Specify GPU devices
                    print(f'Using {len(gpus)} GPUs')
                else:
                    strategy = tf.distribute.OneDeviceStrategy(device='/GPU:0' if gpus else '/CPU:0')
                    print('Using CPU or single GPU')
            else:
                strategy = tf.distribute.OneDeviceStrategy(device='/CPU:0')
                print('No GPU available. Using CPU.')

            with strategy.scope():
                with multiprocessing.Pool(processes=cpu_process) as pool:
                    results = pool.map(partial_process_solution, self.solutions)

                for t in results:
                    if t[1] == self.n:
                        print('Found max :(')
                        return t
                    if t[1] > max_result[1]:
                        max_result = t
                    elif t[1] == max_result[1]:
                        max_result[0].extend(t[0])

                return max_result
        else:
            print('This does not work:', __name__)
            return (list(), 0)
    
    # helper functions:
    def choose_solution_recursive(self, chosen_solutions_ids: list[int], valid_solutions_ids: list[int], chosen_points: list[Point], valid_points: list[Point] = list(), valid_matrix: np.ndarray = np.zeros((0, 0)), options: tuple[bool] = tuple([True, True])):
        current_max = (list([chosen_solutions_ids]), chosen_solutions_ids.__len__())
        if chosen_solutions_ids.__len__() == self.n:
            if options[0] and not options[1]:
                if self.is_solution(chosen_points):
                    return current_max
                else:
                    return (list(), 0)
            return current_max
        elif valid_points.__len__() < 2 * self.n:
            return current_max
        
        z_layer = chosen_solutions_ids.__len__()
        new_valid_matrix = valid_matrix
        
        for new_solution_id in valid_solutions_ids:
            added_points = copy.deepcopy(self.solutions[new_solution_id][1])
            for point in added_points:
                point.z = z_layer
            
            # checking if new solution is valid and adding its points to a list 
            i = 0
            j = 0
            if options[0] == True:
                new_valid_matrix = valid_matrix.copy()
                for point in added_points:
                    new_valid_matrix[point.x, point.y] = new_valid_matrix[point.x, point.y] + 1
            if options[1] == True:
                while i < 2 * self.n and (added_points[i] >= valid_points[j]):
                    if added_points[i] == valid_points[j]:
                        i = i + 1
                        j = j + 1
                    else:
                        j = j + 1
                        
            if i == 2 * self.n or options[1] == False: # solution is valid for current order with options
                new_valid_solutions = valid_solutions_ids
                new_valid_points = valid_points
                
                if options[0]:
                    new_valid_solutions = self.reduce_solution_field_by_validMat(valid_solutions_ids.copy(), new_valid_matrix)
                
                if options[1]:
                    new_valid_points = self.removeInValidPoints_2n_new(chosen_points, added_points, z_layer, valid_points.copy())
                chosen_points.extend(added_points)
                        
                new_chosen_solutions_ids = chosen_solutions_ids.copy()
                new_chosen_solutions_ids.append(new_solution_id)
                t = self.choose_solution_recursive(new_chosen_solutions_ids, new_valid_solutions, chosen_points, new_valid_points, new_valid_matrix, options)
                if t[1] > current_max[1]: # bigger max found, replace the old max
                    current_max = t
                elif t[1] == current_max[1]: # found another solution with the same len
                    current_max[0].extend(t[0])
                if current_max[1] == self.n: # max is at upper bound
                    break
                
                if options[1]:
                    for i in range(2 * self.n):
                        chosen_points.pop()
                        
        return current_max
    
    def reduce_solution_field_by_validMat(self, valid_solutions: list[int], valid_matrix: np.ndarray[int, int]):
        index = 0
        while index in range(valid_solutions.__len__()):
            for point in self.solutions[valid_solutions[index]][1]:
                if valid_matrix[point.x, point.y] >= 2:
                    valid_solutions.pop(index)
                    index = index - 1
                    break
            index = index + 1
        return valid_solutions

    # 2D algorithms:
    def find_max_solutions_2D(self):
        # TODO: integrate multiprocess approach to optimize run time of this algorithm
        max = 2 * self.n           
        valid = self.getAllValidPoints(d = 2)
        max_solutions = (list([self.points]), len(self.points))
        
        if len(self.points) == 0:
            max_solutions = self.choose_2_Xpoints_recursive_from_valid(max, valid, 0, 0)
        else:
            print("ERROR!")
            return (0, 0)
        
        if max_solutions[1] < max:
            print("could not find max solution")
            return max_solutions
        self.solutions = list(enumerate(max_solutions[0]))
        
        return (len(self.solutions), max_solutions[1])
    
    def brute_force(self):
        max = 2 * self.n
        if self.d == 3:
            max = max * self.n
        valid = self.getAllValidPoints(d=self.d)
        current_max = (list([self.points]), len(self.points))
        if len(self.points) == 0:
            for point1, point2 in it.combinations(valid, 2): # no point in choosing one and checking what is valid, everything is. this loop checks combinations of 2 points
                chosen = list([point1, point2])
                t = self.choose_points_recursive(max, chosen, self.getAllValidPoints(d=self.d, chosen=chosen))
                if t[1] > current_max[1]:
                    current_max = t
                elif t[1] == current_max[1] or t[1] == 2 * self.n: # found another solution(at least one) with the same max
                    union_solutions(current_max[0], t[0], current_max[1])
        else:
            current_max = self.choose_points_recursive(max, self.points.copy(), validPoints=valid)
        self.solutions = list(enumerate(current_max[0]))
        return (len(self.solutions), current_max[1])
            
    # helper functions:
    def choose_points_recursive(self, max, chosen_points: list = list(), validPoints: list = list()):
        current_max = (list([list.copy(chosen_points)]), len(chosen_points))
        if current_max[1] == max or len(validPoints) == 0:
            return current_max
        
        for point in validPoints:
            # find sorted location by of 3-dimentional point:
            loc = 0
            while loc < len(chosen_points) and point.z > chosen_points[loc].z:
                loc = loc + 1
            while loc < len(chosen_points) and point.z == chosen_points[loc].z and point.x > chosen_points[loc].x:
                loc = loc + 1
            while loc < len(chosen_points) and point.z == chosen_points[loc].z and point.x == chosen_points[loc].x and point.y > chosen_points[loc].y:
                loc = loc + 1
            if loc == len(chosen_points):
                chosen_points.append(point)
            else:
                chosen_points.insert(loc, point)
            
            # call recursively to choose other points and get the max result:
            new_valid = self.removeInValidPoints_1_new(point, validPoints.copy(), chosen=chosen_points)
            t = self.choose_points_recursive(max, chosen_points=chosen_points, validPoints=new_valid)
            if t[1] > current_max[1]: # bigger max found, replace the old max
                current_max = t
            elif t[1] == current_max[1] or t[1] == max: # found another solution(at least one) with the same max
                union_solutions(current_max[0], t[0], current_max[1])
            chosen_points.remove(point)
        
        return current_max
    
    def choose_2_Xpoints_recursive_from_valid(self, max: int, validPoints: list, x: int, z: int = 0, chosen_points: list = list()):
        current_max = (list([list.copy(chosen_points)]), len(chosen_points) + len(self.points))
        if current_max[1] == max:
            return current_max
        elif len(validPoints) < 2:
            if len(validPoints) == 1:
                current_max[0][0].append(validPoints[0])
            return current_max
        
        for i in range(len(validPoints)):
            if validPoints[i].x != x or validPoints[i].z != z:
                break
            chosen_points.append(validPoints[i])
            
            j = i + 1
            while j < len(validPoints):
                if validPoints[j].x != x or validPoints[j].z != z:
                    break
                chosen_points.append(validPoints[j])
                # call recursively to choose other points and get the max result:
                new_valid = self.removeInValidPoints_2_new(validPoints[i], validPoints[j], validPoints.copy(), chosen=chosen_points)
                if x + 1 == self.n:
                    x = -1
                    z = z + 1
                t = self.choose_2_Xpoints_recursive_from_valid(max, new_valid, x + 1, z, chosen_points=chosen_points)
                if t[1] > current_max[1]: # bigger max found, replace the old max
                    current_max = t
                elif t[1] == current_max[1] or t[1] == max: # found another solution(at least one) with the same max
                    union_solutions(current_max[0], t[0], current_max[1])
                chosen_points.pop()
                j = j + 1
            chosen_points.pop()
        
        return current_max
    
    # TODO: implement choose points probabilisticly from valid points algorithm
    # TODO: implement random greedy algorithm
    # TODO: implement simulated annealing
    # TODO: implement Mean Conflict
    # TODO?: implement neural network(isnt this the other project on this issue? can they elapse?)
    # TODO?: implement Matrix for lines(already did? reduce_solution_field_by_validMat())
        
    def print_grid_2D(self, solutionID: int = -1, mat: np.ndarray[int] = np.zeros((1, 1))):
        if mat.shape == (1, 1):
            mat = np.zeros((self.n, self.n), int)
            points_list = self.points
            if solutionID != -1:
                points_list = self.solutions[solutionID][1]
            for point in points_list:
                mat[point.x, point.y] = mat[point.x, point.y] + 1
            
        for i in range(self.n):
            print(mat[self.n - i - 1, :])
        
    # Grid functions:
    def draw_grid(self, solutionID: list[int] = [-1], axis: str ='off'):
        ticks = np.arange(0, self.n, 1)
        fig = plt.figure(figsize=(12, 10), dpi=80)
        if self.d == 2:
            ax = plt.axes()
        elif self.d == 3:
            ax = plt.axes(projection='3d')
            ax.set_zticks(ticks)
            ax.set_zlim(0, self.n - 1)
            
        ax.set_xticks(ticks)
        ax.set_yticks(ticks)
        # ax.set_xlim(-0.1, self.n - 0.9)
        # ax.set_ylim(-0.1, self.n - 0.9)
        
        
        if self.d == 2:
            for x in range(self.n):
                ax.plot([x, x], [0, self.n - 1], 'grey')
            for y in range(self.n):
                ax.plot([0, self.n - 1], [y, y], 'grey')

            for point in self.points:
                ax.scatter([point.x], [point.y], color='black', s=250)
            if solutionID != -1:
                for point in self.solutions[solutionID]:
                    ax.scatter([point.x], [point.y], color='black', s=250)
            
        elif self.d == 3:
            # paint grid lines:
            
            # paint X-lines:
            for y in range(self.n):
                for z in range(self.n):
                    ax.plot3D([0, self.n - 1], [y, y], [z, z], 'grey')
            
            # paint Y-lines:
            for x in range(self.n):
                for z in range(self.n):
                    ax.plot3D([x, x], [0, self.n - 1], [z, z], 'grey')
            
            # paint Z-lines:
            for x in range(self.n):
                for y in range(self.n):
                    ax.plot3D([x, x], [y, y], [0, self.n - 1], 'grey')        

            # paint lines from (0, 0 ,0) to visualize directions:
            ax.plot3D([0, self.n - 1], [0, 0], [0, 0], 'red') # paint red to visualize X axis
            ax.plot3D([0, 0], [0, self.n - 1], [0, 0], 'green') # green to visualize Y axis
            ax.plot3D([0, 0], [0, 0], [0, self.n - 1], 'blue') # blue to visualize Z axis
            
            for point in self.points: # paint all dots on grid
                ax.scatter([point.x], [point.y], [point.z], color='black', s=250)
            if solutionID[0] != -1:
                z = 0
                for s in solutionID:
                    for point in self.solutions[s][1]:
                        ax.scatter([point.x], [point.y], [z], color='black', s=250)
                    z = z + 1
            
        else:
            print('figure cannot be shown for %d dimentions'.format(self.d))
            
        if axis == 'off':
            plt.axis('off')
        else:
            ax.set_xlabel('X axis')
            ax.set_ylabel('Y axis')
            if self.d == 3:
                ax.set_zlabel('Z axis')
            
        # manager = plt.get_current_fig_manager()
        # manager.full_screen_toggle()
        # ax.margins(0.02)
        plt.show()
        
def union_solutions(set1: list[Point], set2: list[Point], length: int):
        for solution1 in set1:
            for solution2 in set2:
                i = 0
                while i < length and solution1[i] == solution2[i]:
                    i = i + 1
                if i == length:
                    set2.remove(solution2)
            
        # add all valid solutions:
        set1.extend(set2)