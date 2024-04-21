from mesa import Model
from mesa.time import SimultaneousActivation
from mesa import DataCollector
from .solver_agent import SolverAgent
from .GeneticAgent import createGeneticAgent
from .colaboration_types import ColaborationTypes


class MultiAgentSolverModel(Model):
    """
    A multi-agent system model that uses both solver and genetic algorithms to optimize truck delivery routes.
    This class incorporates a variety of agents that can collaborate or compete to find the best solutions under
    different operational constraints and objectives.

    Attributes:
        rand_step_generator (callable): A function to generate random steps for the solver agents.
        step_function_list (list of functions): List of functions defining the steps for solver agents.
        route_id (int): Identifier for the specific set of routes and associated data.
        truckCapacityKg (float): Maximum weight capacity of each truck.
        truckCapacityVol (float): Maximum volume capacity of each truck.
        solution_pool (SolutionPool): Shared pool of solutions that agents can access and update.
        GA_stepSize (int): Number of generations the genetic agent evolves at each step.
        colaboration_type (ColaborationTypes): Defines the type of collaboration among agents (NONE, FRIENDS, ENEMIES).
        QLearn_q (optional): GA specific Parameter. Q-learning object to be used by the GA.
        QLearn_neighbor_function_list (list, optional): GA specific Parameter. Functions to generate neighboring solutions for Q-learning.
        QLearn_eval_function (function, optional): GA specific Parameter. Function to evaluate solution fitness for Q-learning.
        agent_labels (list of str, optional): Labels to assign to solver agents for identification in reports.

    Methods:
        step(): Executes one simulation step, which involves all agents performing their defined actions,
                followed by data collection on their states and the global best solutions.

    Examples:
        >>> model = MultiAgentSolverModel(
                rand_step_generator=lambda: random.randint(1, 10),
                step_function_list=[step_func1, step_func2],
                route_id=101,
                truckCapacityKg=10000,
                truckCapacityVol=100,
                solution_pool=shared_solution_pool,
                GA_stepSize=5,
                colaboration_type=ColaborationTypes.FRIENDS
            )
        >>> model.step()  # Run one step of the model simulation
    """

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
        QLearn_q=None,
        QLearn_neighbor_function_list=None,
        QLearn_eval_function=None,
        agent_labels=[],
    ):
        super().__init__()
        self.schedule = SimultaneousActivation(self)

        self.solution_pool = solution_pool
        self.rand_step_generator = rand_step_generator

        # initializes solver agents based on the step function list it received
        id_counter = 0
        for i in range(len(step_function_list)):
            a = SolverAgent(
                id_counter,
                self,
                rand_step_generator(),
                step_function_list[i],
                colaborative=colaboration_type,
                label="solver_agent" if len(agent_labels) == 0 else agent_labels[i],
            )
            self.schedule.add(a)

            id_counter += 1

        # Genetic Agent Setup
        GApopulationSize = 20
        GA = createGeneticAgent(
            id_counter,
            self,
            route_id,
            GApopulationSize,
            truckCapacityKg,
            truckCapacityVol,
            step_size=GA_stepSize,
            QLearn_q=QLearn_q,
            QLearn_neighbor_function_list=QLearn_neighbor_function_list,
            QLearn_eval_function=QLearn_eval_function,
            collaborative=colaboration_type,
        )

        self.schedule.add(GA)

        # sets up the data colectors

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
                "agent label": lambda a: a.label,
                "agentBest": lambda a: a.current_step.get_best_sol(),
                "agentBestValue": lambda a: a.current_step.get_best_sol_value(),
            },
        )

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
