from collections.abc import Callable
from typing import TypeVar
from solver_step import SolverStep

State = TypeVar('State')   
def taboo_search_solver_factory(get_random_neighbour: Callable[[State],State],
                                state_to_energy: Callable[[State], float],
                                tabu_list_size: int)-> Callable[[SolverStep], SolverStep]:

    def taboo_search_step(init_state: SolverStep)->SolverStep:
        s = init_state.get_best_sol()
        tabu_list = []
        
        for _ in range(init_state.get_step_size()):
            neighbors = [get_random_neighbour(s) for _ in range(tabu_list_size)]
            best_neighbor = min(neighbors, key=state_to_energy)

            if best_neighbor not in tabu_list:
                s = best_neighbor
                tabu_list.append(s)
                if len(tabu_list) > tabu_list_size:
                    tabu_list.pop(0)

        return SolverStep(s, state_to_energy(s), init_state.get_step_size())

    return taboo_search_step