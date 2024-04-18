
import random
from .utils.helperFunctions import *
import heapq

# from loadData import *
from .utils.initializePopulation import initializePopulation
from ..q_learning import q_learning_iteration
from .utils.flattenSolution import *

# # General constant variables
# truckKg = 2e4
# truckVol = 20
# truckSpd = 0.6


def _tournamentSelection(population, tournament_size, mating_pool_size, fitnessScores):
    # Calculate fitness function for every individual in the population
    # fitnessScores = []
    # for individual in population:
    #   fitnessScores.append(fitnessFunction(individual,cost))

    matingPool = []

    while len(matingPool) < mating_pool_size:
        battle = random.sample(list(zip(population, fitnessScores)), tournament_size)

        # winner will be the one with the least amount of cost. he will be selected for the mating pool
        winner = min(battle, key=lambda x: x[1])

        # This intentionally allows multiple individuals from entering the mating_pool
        matingPool.append(winner[0])

    return matingPool


### Order CrossOver:
# In this approach, we select 2 points in the parent sequences to define a child.


def _orderCrossover(parent1, parent2):
    dad = flatten(parent1)
    mom = flatten(parent2)
    child1 = [None] * len(mom)
    child2 = [None] * len(dad)
    minListLength = len(dad) if len(dad) < len(mom) else len(mom)

    # This gets 2 random indices where cx1 is always the smaller and cx2 the bigger
    cx1, cx2 = sorted(random.sample(range(minListLength), 2))

    # Child inheritence from dad and mom
    child1[cx1 : cx2 + 1] = dad[cx1 : cx2 + 1]
    child2[cx1 : cx2 + 1] = mom[cx1 : cx2 + 1]

    # Inherent from mom and dad

    position = 0
    for node in mom:
        # If position is cx1, that means it has already gotten the node from the father
        if position == cx1:
            position = cx2 + 1

        # Just double checking to make sure it stays correct (only 1 visit per node)
        if node not in child1:
            child1[position] = node
            position += 1

    position = 0
    for node in dad:
        # same thing to the dad.
        if position == cx1:
            position = cx2 + 1
        if node not in child2:
            child2[position] = node
            position += 1

    return child1, child2


def _reconstruct_routes(
    flat_sequence, truckCapacityKg, truckCapacityVolume, demandForCustomer
):
    """This function is to just recover the sequence after flattening it"""
    routes = []
    current_route = [0]
    current_weight, current_volume = 0, 0
    # trucks = [[0] * numberOfTrucks]
    # customerRemaining = flat_sequence.copy()
    # while customerRemaining:
    #     for i in range(len(trucks)):
    #         if not customerRemaining:
    #             break
    #         customerChosen = customerRemaining[0]
    #         demand = demandForCustomer[customerChosen]

    #         if canAddCustomerToTruck(
    #             trucks[i], truckKg, truckVol, demand, demandForCustomer
    #         ):
    #             truck.append(customerChosen)
    #             customerRemaining.pop(0)
    # for truck in trucks:
    #     if len(truck) > 1:  # If it has at least one customer
    #         truck.append(0)

    for node in flat_sequence:
        node_weight, node_volume = demandForCustomer[node]

        # Check if adding this node would exceed capacity
        if (
            current_weight + node_weight > truckCapacityKg
            or current_volume + node_volume > truckCapacityVolume
        ):
            # Finish current route and start a new one
            current_route.append(0)  # End with depot
            routes.append(current_route)
            current_route = [0, node]  # Start new route with depot and node
            current_weight, current_volume = node_weight, node_volume
        else:
            # Add node to current route
            current_route.append(node)
            current_weight += node_weight
            current_volume += node_volume

    current_route.append(0)  # End with depot
    routes.append(current_route)

    return routes


def _treatCrossOver(parents, truckCapacityKg, truckCapacityVol, demandForCustomer):
    # if len(parents) % 2 != 0:
    #     print("Not matching crossover")
    #     return -1
    parents1 = parents[: len(parents) // 2]
    parents2 = parents[len(parents) // 2 :]

    population = []
    for dad, mom in zip(parents1, parents2, strict=True):
        (child1, child2) = _orderCrossover(dad, mom)
        route1 = _reconstruct_routes(
            child1, truckCapacityKg, truckCapacityVol, demandForCustomer
        )
        route2 = _reconstruct_routes(
            child2, truckCapacityKg, truckCapacityVol, demandForCustomer
        )
        population.append(route1)
        population.append(route2)
    return population


def _handleQLearning(solution, q, neighbor_function_list, eval_function, epsilon=0.8):
    currentSol = flattenSolution(solution)
    newSolution = q_learning_iteration(
        currentSol, q, neighbor_function_list, eval_function, epsilon
    )
    if(eval_function(currentSol)> eval_function(newSolution)):
        return rebuildFlattenSolution(newSolution)
        
    return rebuildFlattenSolution(currentSol)


# TODO: Apply Q-learning here
def _mutation(
    solution,
    demandForCustomer,
    truckCapacityKg,
    truckCapacityVolume,
    q=None,
    neighbor_function_list=None,
    eval_function=None,
    epsilon=0.8,
):
    if q:
        return _handleQLearning(
            solution, q, neighbor_function_list, eval_function, epsilon
        )

    else:

        # Randomly select one truck
        truck_index = random.randint(0, len(solution) - 1)
        route = solution[truck_index]

        # Ensure there are enough customers for a swap
        # SWAP
        if len(route) > 4:  # More than just depot (start/end) and one customer
            # Randomly select two customers to swap
            customer_index1, customer_index2 = random.sample(
                range(1, len(route) - 1), 2
            )

            # Perform the swap
            route[customer_index1], route[customer_index2] = (
                route[customer_index2],
                route[customer_index1],
            )

            # Check capacity constraints and revert if necessary
            total_weight, total_volume = 0, 0
            for node in route[1:-1]:
                node_weight, node_volume = demandForCustomer[node]
                total_weight += node_weight
                total_volume += node_volume

            # Revert the swap if the mutation results in an infeasible route
            if total_weight > truckCapacityKg or total_volume > truckCapacityVolume:
                route[customer_index1], route[customer_index2] = (
                    route[customer_index2],
                    route[customer_index1],
                )
        return solution


def genetic_algorithm(
    populationSize,
    numberOfTrucks,
    truckCapacityKg,
    truckCapacityVol,
    customersId,
    cost,
    demandForCustomer,
    maxGenNumber=100,
    mutationRate=0.05,
    population=None,
    verbose=False,
    q=None,
    neighbor_function_list=None,
    eval_function=None,
):
    """O(m*n)(AMORTIZED) where m is the number of generations and n is the population number"""
    if population is None:
        # Initializing random population
        population = initializePopulation(
            populationSize,
            numberOfTrucks,
            customersId,
            demandForCustomer,
            truckCapacityKg,
            truckCapacityVol,
        )
        print("population generated")

    generations = 0

    history = []
    while generations < maxGenNumber:
        # Shuffle to avoid dependency on sorting which leads to decrease in genetic variability.
        random.shuffle(population)

        ## MinHeap to keep track of current best and not-so-best solutions.
        fitness_heap = []

        # calculate fitness function
        fitnesses = [fitnessFunction(sol, cost) for sol in population]

        # Calculate 'winners' after selection via tournament
        winners = _tournamentSelection(population, 2, len(population), fitnesses)

        # Crossover
        population = _treatCrossOver(
            winners, truckCapacityKg, truckCapacityVol, demandForCustomer
        )

        # Mutation
        for i in range(len(population)):
            if random.random() < mutationRate:
                population[i] = _mutation(
                    population[i],
                    demandForCustomer,
                    truckCapacityKg,
                    truckCapacityVol,
                    q,
                    neighbor_function_list,
                    eval_function,
                )

        generations += 1

        newFitnesses = [fitnessFunction(sol, cost) for sol in population]
        for i, fitness in enumerate(newFitnesses):
            heapq.heappush(fitness_heap, (fitness, population[i]))

        population = [sol for _, sol in fitness_heap]
        best_fitness, best_solution = fitness_heap[0]
        history.append(best_fitness)
        if verbose and (generations % 10 == 0):
            print(f"Generation {generations}: Best Fitness = {best_fitness}")

    # print(f"Best Solution Found: {best_solution}")
    # print(f"With Fitness: {best_fitness}")
    return best_solution, best_fitness, history, population
