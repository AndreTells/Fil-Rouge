from .selection_functions import standard_selection
import itertools
import numpy as np
import random

def generic_solver_factory(
        initial_population_generator,
        fitness_score_of,
        crossover_sols,
        mutate_sol,
        selection = standard_selection,
        return_history = False
    ):
    def solver(num_iterations,N, mutation_rate):
        population = initial_population_generator(N)
        best_individual = -1
        best_fitness = float('inf')
        history = {'states':[], 'best_fitness':[]}
        for it in range(num_iterations):
            #best = map(lambda x: x[0],ordered_population[:min(N//2,1)])
            best_gen_sol = min(population,key= lambda x:fitness_score_of(x))
            best_gen_fitness = fitness_score_of(best_gen_sol)

            if(return_history):
                history['states'].append(best_gen_sol)
                history['best_fitness'].append(best_gen_fitness)
            
            if(best_gen_fitness <best_fitness):
                best_fitness = best_gen_fitness
                best_individual = best_gen_sol
            
            population_ = []
            for sol in sorted(population, key= lambda x: fitness_score_of(x))[:N]:
                fitness = fitness_score_of(sol)
                while True:
                    new_sol = mutate_sol(sol)
                    new_fitness = fitness_score_of(new_sol)

                    if(new_fitness <= fitness):
                        population_.append(new_sol)
                        break
                    
                    prob = np.exp(
                        -10
                        * (
                            (float)(new_fitness - fitness)
                            / (num_iterations-it)
                        ),
                    )

                    if(prob > mutation_rate):
                        population_.append(new_sol)
                        population_.append(sol)
                        break

            population = population_

        if(return_history):
            return best_individual, history
        return best_individual

    return solver 