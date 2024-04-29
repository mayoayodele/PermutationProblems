import dimod
import numpy as np
from Problems.Problem_QAP import Problem_QAP
from dwave.system import LeapHybridCQMSampler
from cqm_methods import cqm_methods


def main():
    time_limit = 20


    for problem_name in [ # 'had12', 'had14', 'had16', 'had18', 'had20', 'rou12', 'rou15', 'rou20', 
                         'tai40a', 'tai40b', 'tai50a', 'tai50b' , 'tai60a', 'tai60b' 
    ]:
        path = 'Problems/QAP//' + problem_name+ '.txt' 
        qap = Problem_QAP(path)
        problem_size = qap.problem_size


        
        model = [[dimod.Binary( 'position' + str(j) + 'location' + str(i) ) for i in range(problem_size)] for j in range(problem_size)]
        
        cqm = dimod.ConstrainedQuadraticModel()
        cqm.set_objective(cqm_methods.f_qap(model, qap.flow_matrix,  qap.distance_matrix, problem_size))

        cqm.add_constraint(cqm_methods.g1(model, problem_size)  == 0, label = 'constraint_column')
        cqm.add_constraint(cqm_methods.g2(model, problem_size)  == 0, label = 'constraint_row')
        
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