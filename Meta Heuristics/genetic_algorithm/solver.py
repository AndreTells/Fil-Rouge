from .selection_functions import standard_selection
import itertools

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
        best_fitness = -float('inf')
        history = {'states':[], 'best_fitness':[]}
        for _ in range(num_iterations):
            fitness_scores = [fitness_score_of(x) for x in population]
            #best = map(lambda x: x[0],ordered_population[:min(N//2,1)])
            best_gen_fitness = max(fitness_scores)
            if(return_history):
                history['states'].append(population[fitness_scores.index(best_gen_fitness)])
                history['best_fitness'].append(best_gen_fitness)

            
            if(best_gen_fitness >best_fitness):
                best_fitness = best_gen_fitness
                best_individual = population[fitness_scores.index(best_fitness)]
            
            population_ = []
            while len(population)>0:
                parent1, parent2 = selection(population, fitness_scores)
                #print(parent1, parent2,child1, child2)
                child1 = mutate_sol(parent1, mutation_rate)
                child2 = mutate_sol(parent2, mutation_rate)
    
                population_.append(child1)
                population_.append(child2)
                
            population = population_

        if(return_history):
            return best_individual, history
        return best_individual

    return solver 