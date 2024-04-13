from mesa.agent import Agent
from geneticAlgorithm import genetic_algorithm

# from ..solver_step import SolverStep


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
        collaborative=False,
        allowWorseSolution=False,
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
        self.bestFitness = float("inf")
        self.bestSolution = None
        self.history = []
        # self.current_step = SolverStep()

    def share_step(self, step):
        self.current_step = self.model.solution_pool.get_best_sol()
        if self.current_step == None:
            self.current_step = self.model.rand_step_generator()
        return

    def step(self):
        self.bestSolution, self.bestFitness, self.history, self.population = (
            genetic_algorithm(
                self.populationSize,
                self.numberOfTrucks,
                self.truckCapacityKg,
                self.truckCapacityVol,
                self.customersId,
                self.cost,
                self.demandForCustomer,
                1,
                mutationRate=0.12,
                population=self.population,
            )
        )

    def get_help(self):
        self.current_step
