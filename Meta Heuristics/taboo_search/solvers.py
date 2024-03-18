from random import uniform
from .vrp_functions import vrp_function_config
from .acceptance_prob_functions import standard_acceptance_prob_function

def taboo_search_solver_factory(get_initial_state, get_random_neighbour,
                                state_to_energy, tabu_list_size,
                                debug_mode=False, return_history=False):
    def taboo_search(max_iterations, tabu_list_size):
        s = get_initial_state()
        tabu_list = []
        history = {'current_energy': [], 'state': [], 'tabu_list_size': []}

        if debug_mode:
            print('The maximum iterations is:', max_iterations)
            print('The initial state is:', s)
            print('------------------------------------------------------')

        for _ in range(max_iterations):
            neighbors = [get_random_neighbour(s) for _ in range(tabu_list_size)]
            best_neighbor = min(neighbors, key=state_to_energy)

            if best_neighbor not in tabu_list:
                s = best_neighbor
                tabu_list.append(s)
                if len(tabu_list) > tabu_list_size:
                    tabu_list.pop(0)

            if return_history:
                history['current_energy'].append(state_to_energy(s))
                history['state'].append(s)
                history['tabu_list_size'].append(len(tabu_list))

            if debug_mode:
                print('The current state is:', s, ' with energy: ',
                      state_to_energy(s))
                print('The tabu list is:', tabu_list)
                print('------------------------------------------------------')

        if return_history:
            return s, history

        return s

    return lambda max_iterations: taboo_search(max_iterations, tabu_list_size)

def VRP_solver_factory(adjacency_matrix, demand_list, delivery_window_list, capacity):
    function_dict = vrp_function_config['standard']
    tabu_list_size = 10  # Define the size of the taboo list
    solver = taboo_search_solver_factory(
        lambda: function_dict['init_function'](
            adjacency_matrix, demand_list, capacity,
            function_dict['capacity_add'],
            function_dict['capacity_null_value'],
            lambda current_load, capacity, node, current_path_dist:
            function_dict['capacity_condition'](
                current_load, capacity, node, current_path_dist,
                delivery_window_list
            )
        ),
        lambda x: function_dict['get_neighbour'](x, adjacency_matrix),  # get random neighbour
        lambda x: function_dict['state_to_energy'](x,
                                                   adjacency_matrix, demand_list, capacity,
                                                   function_dict['capacity_add'],
                                                   function_dict['capacity_null_value'],
                                                   lambda current_load, capacity, node, current_path_dist:
                                                   function_dict['capacity_condition'](
                                                       current_load, capacity, node, current_path_dist,
                                                       delivery_window_list
                                                   )),
        tabu_list_size,  # Provide tabu_list_size argument
        return_history=True
    )
    return solver
