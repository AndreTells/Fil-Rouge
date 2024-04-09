from mesa.agent import Agent


class GeneticAgent(Agent):
    def __init__(
        self,
        uniqueId,
        model,
        initialPopulation,
        collaborative=False,
        allowWorseSolution=False,
    ):
        super().__init__(uniqueId, model)
        self.initialPopulation = initialPopulation
        self.collaborative = collaborative
        self.allowWorseSolution = allowWorseSolution

    def share_step(self, step):
        model.solution_pool.add_solution(step)
        return
