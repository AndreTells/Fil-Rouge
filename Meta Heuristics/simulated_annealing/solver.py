from random import uniform
from .temperature_functions import *
from .probability_functions import *

def generic_solver_factory( get_initial_state,
                            get_random_neighbour,
                            state_to_energy,
                            calculate_temperature = temperature_standard,
                            acceptance_prob_function = probability_standard,
                            debug_mode = False,
                            return_history = False):
    def simulated_annealing(k_max):
        s = get_initial_state()
        history = {'temperature':[], 'current_energy':[], 'state':[]}
        if(debug_mode):
            print('The maximum k is:', k_max)
            print('The initial state is:', s)
            print('------------------------------------------------------')
        for k in range(k_max):
            
            temp = calculate_temperature(1-((k+1)/k_max))
            s_new = get_random_neighbour(s)
            energy_of_s = state_to_energy(s)
            energy_of_s_new = state_to_energy(s_new)
            res_acceptance_prob_function = acceptance_prob_function(energy_of_s,energy_of_s_new, temp)
            limit = uniform(0,1) 
            if(debug_mode):
                print('The current temperature is:', temp)
                print('The current state is:', s, ' with energy: ', energy_of_s)
                print('The new state is    :', s_new, ' with energy: ', energy_of_s_new)
                print('The result of the acceptance probability function is:', res_acceptance_prob_function )
                print('The limit of acceptance for the new state is:', limit)
                print('------------------------------------------------------')
            if(return_history):
                history['temperature'].append(temp)
                history['current_energy'].append(energy_of_s)
                history['state'].append(s)
            if res_acceptance_prob_function >= limit:
                s = s_new

        if(return_history):
            return s, history

        return s

    return simulated_annealing

'''
def VRP_solver_factory(adjacency_matrix, demand_list, delivery_window_list, capacity):
    function_dict = vrp_function_config['standard']

    solver = generic_solver_factory(
                lambda: function_dict['init_function'](
                      adjacency_matrix, demand_list, capacity,
                      function_dict['capacity_add'],
                      function_dict['capacity_null_value'],
                      lambda current_load,capacity, node, current_path_dist: 
                        function_dict['capacity_condition'](
                        current_load,capacity, node, current_path_dist,
                        delivery_window_list
                        )
                ),                              # initial value 
                lambda x: function_dict['get_neighbour'](x, adjacency_matrix),     # get random neighbour
                lambda x: function_dict['state_to_energy'](x,
                      adjacency_matrix, demand_list, capacity,
                      function_dict['capacity_add'],
                      function_dict['capacity_null_value'],
                      lambda current_load,capacity, node, current_path_dist: 
                        function_dict['capacity_condition'](
                        current_load,capacity, node, current_path_dist,
                        delivery_window_list
                        )),
                    return_history = True)

    return solver
'''
