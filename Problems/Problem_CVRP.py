import math
import vrplib
import numpy as np

class Problem_CVRP:
    def __init__(self, path):
        """Several CVRP formats are read during initialisation

        Args:
            path (String): The path to the problem file

        Raises:
            Exception: Unsupported  format
        """
        try:
            instance = vrplib.read_instance(path)
            self.solution = vrplib.read_solution(path.replace('.vrp', '.sol'))
            properties = instance['comment'].split()

            coord = instance['node_coord']
            if instance['edge_weight_type'] =='EUC_2D':
                dist = Problem_CVRP.dist_euclidean


            D = Problem_CVRP.create_matrix(coord, dist)
            self.problem_size = instance['dimension']
            self.distance_matrix= D
            self.optimal = int(properties[-1].split(')')[0])
            self.n_trucks = int(properties[properties.index( 'trucks:') +1].split(',')[0])
            self.demand = instance['demand']
            self.depot = instance['depot']
            self.instance = instance
            
            
        except:
            print('Unsupported CVRP format')
            raise NotImplementedError


    @staticmethod
    def create_matrix(coord, dist):
        n = len(coord)
        matrix = np.zeros(shape = (n, n), dtype = int)
        for i in range(n-1):
            for j in range(i+1, n):
                matrix[i,j] = dist(coord[i], coord[j])
                matrix[j,i] = dist(coord[i], coord[j])
        return matrix 


    
    @staticmethod
    def dist_manhathan(coord1, coord2):
        x1, y1 = coord1
        x2, y2 = coord2
        return int(abs(x2-x1) + abs(y2-y1)) + 0.5

    @staticmethod
    def dist_euclidean(coord1, coord2):
        x1, y1 = coord1
        x2, y2 = coord2
        return (math.sqrt((x2-x1)**2 + (y2 - y1)**2)) + 0.5




    def f_sub(self, solution):
        """This function calculates the total distance for a given list of locations

        Args:
            solution (list): the list of location indices

        Returns:
            int: the sum of distance
        """
        #add the first fixed city
        distance= self.distance_matrix[0, solution[0]]
        for i in range(len(solution)-1):
            distance+= self.distance_matrix[solution[i], solution[i+1]]
        #go back to first city
        distance += self.distance_matrix[solution[-1], 0]
        return distance
    


    def f(self, routes):
        """This function calculates the total distance for a given list of routes

        Args:
            routes ("2D list"): a list of routes, each route is a list of locations

        Returns:
            int: the sum of distances
        """
        return sum([self.f_sub(route) for route in routes])