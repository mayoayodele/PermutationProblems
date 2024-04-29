
class Problem_QAP:
    def __init__(self, path):
        f = open(path, "r")
        file_content = f.read().splitlines()
        file_reader_counter = 0
        problem_properties = file_content[file_reader_counter].split()
        file_reader_counter+=2

        self.problem_size = int(problem_properties[0])
        try:
            self.best_known = int(problem_properties[1])
        except:
            self.best_known = None

        self.flow_matrix = [file_content[file_reader_counter + i].split() for i in range(self.problem_size)]
        
        try:
            self.distance_matrix= [file_content[file_reader_counter + self.problem_size + 1+ i].split() for i in range(self.problem_size)]
        except:
            self.distance_matrix= [file_content[file_reader_counter + self.problem_size + i].split() for i in range(self.problem_size)]

        for i in range(len(self.flow_matrix)):
            for j in range(len(self.flow_matrix[0])):
                self.flow_matrix[i][j] = int(self.flow_matrix[i][j])

        for i in range(len(self.distance_matrix)):
            for j in range(len(self.distance_matrix[0])):
                self.distance_matrix[i][j] = int(self.distance_matrix[i][j])


    def get_objective_function(self, solution):
        obj = sum([int(self.flow_matrix[i][j])*int(self.distance_matrix[solution[i]][solution[j]]) for j in range(self.problem_size) for i in range(self.problem_size)])
        return obj


