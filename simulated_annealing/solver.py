from random import uniform
from .temperature_functions import *
from .probability_functions import *
from solver_step import SolverStep

# generates a function to solve a given problem using simulated annealing
def generic_solver_factory( get_random_neighbour,
                            state_to_energy,
                            calculate_temperature = temperature_standard,
                            acceptance_prob_function = probability_standard):

    # executes the simulated annealing algorithm for a given solver step 
    # returns a solver step 
    def simulated_annealing_step(init_state):
        s = init_state.get_best_sol().copy()
        k_max = init_state.step_size
        for k in range(k_max):
            temp = calculate_temperature(1-((k+1)/k_max))
            s_new = get_random_neighbour(s)
            energy_of_s = state_to_energy(s)
            energy_of_s_new = state_to_energy(s_new)
            res_acceptance_prob_function = acceptance_prob_function(energy_of_s,energy_of_s_new, temp)
            limit = uniform(0,1)
            if res_acceptance_prob_function >= limit:
                s = s_new
        return SolverStep(init_state.get_step_count()+1,s, state_to_energy(s),init_state.get_step_size())

    return simulated_annealing_step