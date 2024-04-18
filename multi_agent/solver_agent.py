from mesa import Agent
from .colaboration_types import ColaborationTypes


class SolverAgent(Agent):
    def __init__(
        self,
        unique_id,
        model,
        init_step,
        step_function,
        colaborative=ColaborationTypes.NONE,
        label = 'solver_agent'
    ):
        super().__init__(unique_id, model)
        self.current_step = init_step
        self.step_function = step_function
        self.colaborative = colaborative
        self.label = label

    #gets the best solution available in the solution pool, if it exists
    def get_help(self):
        self.current_step = self.model.solution_pool.get_best_sol()
        if self.current_step == None:
            self.current_step = self.model.rand_step_generator()
        return

    #checks if the agent has the best solution in the solution pool and, if not, execute a step to try and reach it
    def compare_With_best(self):
        best_sol = self.model.solution_pool.get_best_sol()
        if best_sol == None:
            return

        if self.current_step.get_best_sol_value() > best_sol.get_best_sol_value():
            new_step = self.step_function(self.current_step)
            self.current_step = (
                new_step
                if new_step.get_best_sol_value()
                < self.current_step.get_best_sol_value()
                else self.current_step
            )

        return

    def step(self):
        match (self.colaborative):
            case ColaborationTypes.FRIENDS:
                self.get_help()

            case ColaborationTypes.ENEMIES:
                self.compare_With_best()

        new_step = self.step_function(self.current_step)

        self.current_step = (
            new_step
            if new_step.get_best_sol_value() < self.current_step.get_best_sol_value()
            else self.current_step
        )

        if self.colaborative != ColaborationTypes.NONE:
            self.model.solution_pool.add_solution(new_step)
