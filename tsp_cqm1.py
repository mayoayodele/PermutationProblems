import dimod
import numpy as np
from Problems.Problem_TSP import Problem_TSP
from dwave.system import LeapHybridCQMSampler
from cqm_methods import cqm_methods


def main():
    time_limit = 10
    for problem_name in [  'gr17', 'gr21', 'gr24', 'fri26','bayg29', 'bays29', 
     #'dantzig42', 'berlin52', 'brazil58',  'st70', 'rd100',   'kroA100', 'kroB100', 'pr107',  'gr120'
    ]:
        path = 'Problems/TSP//' + problem_name+ '.tsp' 
        tsp = Problem_TSP(path)
        problem_size = tsp.problem_size
        reduced_size = problem_size -1 #fix first city
        distance = np.array(tsp.distance_matrix, dtype = 'int64')

        model = [[dimod.Binary( 'position' + str(j) + 'city' + str(i) ) for i in range(reduced_size)] for j in range(reduced_size)]
        cqm = dimod.ConstrainedQuadraticModel()
  

        cqm.set_objective(cqm_methods.f_tsp(model, distance, reduced_size))

        cqm.add_constraint(cqm_methods.g1(model, reduced_size)  == 0, label = 'constraint_column')
        cqm.add_constraint(cqm_methods.g2(model, reduced_size)  == 0, label = 'constraint_row')
        
        sampler = LeapHybridCQMSampler() 

        n_runs = 20
        energies = []
        for i in range(n_runs):
            sampleset = sampler.sample_cqm(cqm, time_limit=time_limit)  
            feasible_sampleset = sampleset.filter(lambda row: row.is_feasible)  
            energy = feasible_sampleset.first.energy
            energies.append(energy)


        print(problem_name, np.mean(energies), np.std(energies))


if __name__ == "__main__":
    main()