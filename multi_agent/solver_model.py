from mesa import Model
from mesa.time import SimultaneousActivation
from mesa import DataCollector
from .solver_agent import SolverAgent
from .GeneticAgent import createGeneticAgent
from .colaboration_types import ColaborationTypes


class MultiAgentSolverModel(Model):
    def __init__(
        self,
        rand_step_generator,
        step_function_list,
        route_id,
        truckCapacityKg,
        truckCapacityVol,
        solution_pool,
        GA_stepSize,
        colaboration_type=ColaborationTypes.NONE,
        q=None,
        neighbor_function_list=None,
        eval_function=None,
    ):
        super().__init__()
        self.schedule = SimultaneousActivation(self)

        self.solution_pool = solution_pool
        self.rand_step_generator = rand_step_generator

        id_counter = 0
        for step_function in step_function_list:
            a = SolverAgent(
                id_counter,
                self,
                rand_step_generator(),
                step_function,
                colaborative=colaboration_type,
            )
            self.schedule.add(a)

            id_counter += 1

        # Genetic Agent Setup
        GApopulationSize = 50
        GA = createGeneticAgent(
            id_counter,
            self,
            route_id,
            GApopulationSize,
            truckCapacityKg,
            truckCapacityVol,
            step_size=GA_stepSize,
            q=q,
            neighbor_function_list=neighbor_function_list,
            eval_function=eval_function,
            collaborative=ColaborationTypes.FRIENDS,
        )
        self.schedule.add(GA)

        def compute_global_best_state(model):
            best_sol = None
            best_sol_val = float("inf")

            for agent in model.schedule.agents:
                sol_val = agent.current_step.get_best_sol_value()
                if sol_val < best_sol_val:
                    best_sol = agent.current_step.get_best_sol()

                    best_sol_val = sol_val

            return best_sol

        def compute_global_best_value(model):
            best_sol = None
            best_sol_val = float("inf")

            for agent in model.schedule.agents:
                sol_val = agent.current_step.get_best_sol_value()
                if sol_val < best_sol_val:
                    best_sol = agent.current_step.get_best_sol()
                    best_sol_val = sol_val

            return best_sol_val

        self.datacollector = DataCollector(
            model_reporters={
                "TheGlobalBest": compute_global_best_state,
                "TheGlobalBestValue": compute_global_best_value,
            },
            agent_reporters={
                "Best": lambda a: a.current_step.get_best_sol_value(),
                "solution": lambda a: a.current_step.get_best_sol(),
            },
        )

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
