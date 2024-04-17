import pandas as pd
from mesa.agent import Agent
from .genetic_algorithm.geneticAlgorithm import genetic_algorithm
from solver_step import SolverStep
from .genetic_algorithm.loadData import getData
from .colaboration_types import ColaborationTypes
from .genetic_algorithm.utils.flattenSolution import *


class GeneticAgent(Agent):
    def __init__(
        self,
        uniqueId,
        model,
        populationSize,
        numberOfTrucks,
        truckCapacityKg,
        truckCapacityVol,
        customersId,
        cost,
        demandForCustomer,
        initialPopulation=None,
        collaborative=ColaborationTypes.NONE,
        allowWorseSolution=False,
        stepSize=1,
        mutation_rate=0.12,
        enemiesGenerationsTolerance=30,
        q=None,
        neighbor_function_list=None,
        eval_function=None,
    ):
        super().__init__(uniqueId, model)
        self.population = initialPopulation
        self.collaborative = collaborative
        self.allowWorseSolution = allowWorseSolution
        self.populationSize = populationSize
        self.numberOfTrucks = numberOfTrucks
        self.truckCapacityKg = truckCapacityKg
        self.truckCapacityVol = truckCapacityVol
        self.customersId = customersId
        self.cost = cost
        self.demandForCustomer = demandForCustomer
        self.history = []
        self.stepSize = stepSize
        (self.best_overall_solution, self.best_current_solution) = (None, None)
        (self.bestFitness, self.current_best_fitness) = (float("inf"), float("inf"))
        self.current_step = SolverStep(None, float("inf"), stepSize)
        self.generations = 0
        self.mutation_rate = mutation_rate
        self.enemyTolerance = enemiesGenerationsTolerance
        self.q = q
        self.neighbor_function_list = neighbor_function_list
        self.eval_function = eval_function
        self.label = 'genetic algorithm'

    # def flattenSolution(self, solution):
    #     # Flattens the array to be in the format : 0,1,2,0,3,2,0,2,1,0
    #     flattenedArray = []
    #     for truck in solution[:-1]:  # Exclude last solution
    #         flattenedArray.extend(truck[:-1])  # Exclude trailing zero
    #     flattenedArray.extend(solution[-1])  # Include last solution
    #     return flattenedArray

    # def rebuildFlattenSolution(self, flattenSol):
    #     trucks = []
    #     truck = [0]
    #     for elem in flattenSol[1:]:  # Exclude start zero
    #         if elem == 0:
    #             truck.append(0)
    #             trucks.append(truck)
    #             truck = [0]
    #         else:
    #             truck.append(elem)
    #     return trucks

    def handleEnemies(self, generationTolerance):
        """This function has a patience limit. It will try to find a better solution by adding generationTolerance // 2 generations. If not successful, double mutation_rate to add genetic variability and run for another generationTolerance // 2 generations."""
        bestSol = self.model.solution_pool.get_best_sol()
        # Fill up solution pool
        if bestSol is None:
            self.nextGen(self.mutation_rate)
            return
        fitnessToBeat = bestSol.get_best_sol_value()

        i = 0
        while (i < (generationTolerance // 2)) and (
            self.current_best_fitness >= fitnessToBeat
        ):
            self.nextGen(self.mutation_rate)
            i += 1

        while i < generationTolerance and self.current_best_fitness >= fitnessToBeat:
            self.nextGen(2 * self.mutation_rate)
            i += 1

        # # Update pool in case I found a better solution
        # if self.current_best_fitness < fitnessToBeat:
        #     solution = flattenSolution(self.current_best_solution)

    def nextGen(self, mutation_rate):
        (
            self.current_best_solution,
            self.current_best_fitness,
            self.history,
            self.population,
        ) = genetic_algorithm(
            self.populationSize,
            self.numberOfTrucks,
            self.truckCapacityKg,
            self.truckCapacityVol,
            self.customersId,
            self.cost,
            self.demandForCustomer,
            self.stepSize,
            mutationRate=mutation_rate,
            population=self.population,
            q=self.q,
            neighbor_function_list=self.neighbor_function_list,
            eval_function=self.eval_function,
        )
        # if self.generations > 0:

        # If found better solution, update the corresponding attributes
        if self.current_best_fitness < self.bestFitness:
            self.best_overall_solution = self.current_best_solution
            self.current_step.state = flattenSolution(self.current_best_solution)
            self.current_step.state_value = self.current_best_fitness
            self.bestFitness = self.current_best_fitness

        # It's necessary to fill the solution_pool in case of collaboration
        if self.collaborative != ColaborationTypes.NONE:
            step = SolverStep(
                flattenSolution(self.current_best_solution),
                self.current_best_fitness,
                self.stepSize,
            )
            self.model.solution_pool.add_solution(step)
        self.generations += 1

    def next_step(self):
        i = 0
        while i < self.stepSize:
            self.nextGen(mutation_rate=self.mutation_rate)
            i += 1

    def update_population(self):
        pool = self.model.solution_pool.pool.copy()
        if self.population and pool:
            # self.population is ordered by fitness values !
            # Keeps the best performance solutions while switches the worst performing ones with the ones in the solution pool
            invalidCount = 0
            for sol in pool:
                formattedSol = rebuildFlattenSolution(sol.get_best_sol())
                if len(formattedSol) > self.numberOfTrucks:
                    invalidCount += 1
            if invalidCount == len(pool):
                return

            self.population = self.population[: -(len(pool) - invalidCount)]

            for flattenedSolution in pool:
                sol = rebuildFlattenSolution(flattenedSolution.get_best_sol())
                if len(sol) > self.numberOfTrucks:
                    continue

                (self.population).append(sol)
            self.population = self.population[: self.populationSize]
        return

    def step(self):
        match (self.collaborative):
            case ColaborationTypes.FRIENDS:
                self.update_population()

            case ColaborationTypes.ENEMIES:
                self.handleEnemies(self.enemyTolerance)
                return
        self.next_step()


def createGeneticAgent(
    agentId,
    model,
    routeId,
    populationSize,
    truckCapacityKg,
    truckCapacityVol,
    step_size=1,
    collaborative=ColaborationTypes.NONE,
    generationsToTolerateEnemies=30,
    QLearn_q=None,
    QLearn_neighbor_function_list=None,
    QLearn_eval_function=None,
):
    customersDf = pd.read_excel("data/2_detail_table_customers.xls")
    depotsDf = pd.read_excel("data/4_detail_table_depots.xls")
    trucksDf = pd.read_excel("data/3_detail_table_vehicles.xlsx")
    numberOfTrucks, customers, cost, demand = getData(
        routeId, customersDf, depotsDf, trucksDf
    )
    agent = GeneticAgent(
        agentId,
        model,
        populationSize,
        numberOfTrucks,
        truckCapacityKg,
        truckCapacityVol,
        customers,
        cost,
        demand,
        stepSize=step_size,
        q=QLearn_q,
        neighbor_function_list=QLearn_neighbor_function_list,
        eval_function=QLearn_eval_function,
        collaborative=collaborative,
        enemiesGenerationsTolerance=generationsToTolerateEnemies,
        initialPopulation=None,
    )
    return agent