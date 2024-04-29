import math
import numpy as np

class Problem_TSP:
    def __init__(self, path):
        """Several tsp formats are read during initialisation

        Args:
            path (String): The path to the problem file

        Raises:
            Exception: Unsupported TSP format
        """
        problem_dict = {}
        try:
            f = open(path, "r")
            is_explicit = False
            line = f.readline() 
            while line.find("DIMENSION") == -1:
                line = f.readline()
            problem_size = int(line.split()[-1])

            
            while line.find("EDGE_WEIGHT_TYPE") == -1:
                line = f.readline()

            if line.find("EUC_2D") != -1:
                dist = Problem_TSP.dist_euclidean
            elif line.find("MAN_2D") != -1:
                dist = Problem_TSP.dist_manhathan
            elif line.find("EXPLICIT") != -1:
                is_explicit = True
                isfull = False
                islower = False
                isupper = False
                while line.find("EDGE_WEIGHT_FORMAT") == -1:
                    line = f.readline()
                if(line.find('FULL_MATRIX') != -1):
                    isfull = True
                elif(line.find('LOWER_DIAG_ROW') != -1):
                    islower = True
                elif(line.find('UPPER_ROW') != -1):
                    isupper = True
                else:
                    print ("Format not implemented")
                    print('works for TSPLIB format based on 2D euclidean, manhattan distances or explicit (FULL_MATRIX and LOWER_DIAG_ROW) matrices')
                    raise Exception      
            else:
                print ("Format not implemented")
                print('works for TSPLIB format based on 2D euclidean, manhattan distances or explicit (FULL_MATRIX and LOWER_DIAG_ROW) matrices')
                raise Exception
            
            if(is_explicit):
                file_content = f.read().splitlines()
                file_content = [_.strip() for _ in file_content ]
                start_index = file_content.index('EDGE_WEIGHT_SECTION')
                try:
                    end_index = file_content.index('DISPLAY_DATA_SECTION')
                except:
                    end_index = file_content.index('EOF')
                lines = file_content[start_index+1:end_index]
                D = Problem_TSP.create_matrix_explicit(lines, problem_size, isfull = isfull, islower= islower, isupper = isupper)   
            else:
                while line.find("NODE_COORD_SECTION") == -1:
                    line = f.readline()

                xy_positions = []
                while 1:
                    line = f.readline()
                    if line.find("EOF") != -1: break
                    (i,x,y) = line.split()
                    x = float(x)
                    y = float(y)
                    xy_positions.append((x,y))

                D = Problem_TSP.create_matrix(xy_positions, dist)

            problem_dict['Problem Size'] = len(D)
            problem_dict['Distance Matrix'] = D
            self.problem_size = int(len(D))
            self.distance_matrix= D
        except:
            print('Unsupported TSP format')
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
    def create_matrix_explicit(file_content, problem_size, isfull = False, islower = False, isupper = False):
        matrix = []
        n = problem_size
        if (isfull):
            for i in range(n):
                line= file_content[i]
                matrix.append([int(__) for __ in line.split()])
        elif(islower):   
            matrix = np.zeros(shape = (n, n), dtype = int)
            lines= []
            for k in file_content:
                lines.extend([int(__) for __ in k.split()])
            
            index = 0
            for i in range(n):
                for j in range(i+1):
                    matrix[i,j]= lines[index]
                    matrix[j,i]= lines[index]
                    index +=1
        elif(isupper):   
            matrix = np.zeros(shape = (n, n), dtype = int)
            lines= []
            for k in file_content:
                lines.extend([int(__) for __ in k.split()])
            
            
            index = 0
            matrix_temp = []
            for i in range(n):
                temp = lines[index:index+n-i-1]
                index = index+n-i-1
                k = np.zeros(n)
                if(len(temp)>0):
                    k[-len(temp):] = temp
                matrix_temp.append(k)
                
            for i in range(n):
                for j in range(i+1, n):
                    matrix[j,i] = matrix_temp[i][j]
                    matrix[i,j] = matrix_temp[i][j]
        
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







    def f(self, solution):
        """This function calculates the objective function for a given list of cities

            Args:
                solution (list): the list of location indices

            Returns:
                int: the sum of distance
        """
        distance= self.distance_matrix[solution[-1]][solution[0]]
        for i in range(len(solution)-1):
            distance+= self.distance_matrix[solution[i]][solution[i+1]]
        return distance


    
    def f_fixed_first_city(self, solution):
        """This function calculates the objective function for a given list of cities (number of cities is reduced by 1 assuming the first city is fixed to city 0)

        Args:
            solution (list): the list of location indices

        Returns:
            int: the sum of distance
        """
        #added 1 to all values from the solution to shift the location index by 1 since we fixed the first city so index 0 refers to location 1
        #add the first fixed city
        distance= self.distance_matrix[0, solution[0] +1]
        for i in range(0, self.problem_size-2):
            distance+= self.distance_matrix[solution[i]+1, solution[i+1] +1]
        #go back to first city
        distance += self.distance_matrix[solution[-1] +1, 0]
        return distance