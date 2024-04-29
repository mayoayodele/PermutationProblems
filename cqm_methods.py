
class cqm_methods:
    @staticmethod
    def f_tsp(x, distance, problem_size):
        """The function calculates the objective function of the problem

        Args:
            x (2D list of dimod.Binary): A permutation matrix representing the solution to the problem
            distance (2D numpy array): A matrix representing the distance between any two locations

        Returns:
            int: the tour length
        """

        #distance between fixed first city and whatever city comes first in the solution
        city_1 = 0
        sum_distance = sum([distance[city_1,city_2+1] * x[0][city_2] for city_2 in range(problem_size)])

        #distance between last selected city and the fixed first city
        sum_distance += sum([distance[city_2+1,city_1] * x[problem_size-1][city_2] for city_2 in range(problem_size)])

        for city_a in range(problem_size):
            for city_b in range(problem_size):
                for position in range(problem_size-1):
                    sum_distance += distance[city_a+1,city_b+1] * x[position][city_a] * x[position+1][city_b]

        return sum_distance

    def f_qap(solution, flow_matrix,  distance_matrix, problem_size):
        """The function calculates the objective function of the problem

        Args:
            x (2D list of dimod.Binary): A permutation matrix representing the solution to the problem
            distance (2D numpy array): A matrix representing the distance between any two locations

        Returns:
            int: objective function
        """
        sum_obj = 0
        for i in range(problem_size):
            for j in range(problem_size):
                for pos_i in range(problem_size):
                    for pos_j in range(problem_size):
                        sum_obj += flow_matrix[i][j] * distance_matrix[pos_i][pos_j] * solution[i][pos_i] * solution[j][pos_j]
        return sum_obj

    def g1(x, problem_size):
        """The function calculates a constraint function of the problem

        Args:
            x (2D list of dimod.Binary): A permutation matrix representing the solution to the problem

        Returns:
            int: the violation of the constraint that all columns of x sum to 1
        """
        sum_column = sum([(sum([x[i][j] for i in range(problem_size)]) -1)**2 for j in range(problem_size)])
        return sum_column



    def g2(x, problem_size):
        """The function calculates a constraint function of the problem

        Args:
            x (2D list of dimod.Binary): A permutation matrix representing the solution to the problem

        Returns:
            int: the violation of the constraint that all rows of x sum to 1
        """
        sum_column = sum([(sum([x[j][i] for i in range(problem_size)]) -1)**2 for j in range(problem_size)])
        return sum_column
