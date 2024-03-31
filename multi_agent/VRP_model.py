from mesa import Model
from mesa.time import SimultaneousActivation
from mesa import DataCollector
from .VRP_agent import VRPSolverAgent

class VRPSolutionModel(Model):
    def __init__(
        self,
        init_step,
        step_function_list,
        solution_pool):
        super().__init__()
        self.schedule=SimultaneousActivation(self)
        
        self.solution_pool = solution_pool

        id_counter = 0
        for step_function in step_function_list:
            a = VRPSolverAgent(id_counter,self,init_step, step_function)
            self.schedule.add(a)
            id_counter +=1

        def compute_global_best_state(model):
            best_sol = None
            best_sol_val = float('inf')

            for agent in model.schedule.agents:
                sol_val = agent.current_step.get_best_sol_value()
                if(sol_val < best_sol_val):
                    best_sol = agent.current_step.get_best_sol()
                    best_sol_val = sol_val
            
            return best_sol

        def compute_global_best_value(model):
            best_sol = None
            best_sol_val = float('inf')

            for agent in model.schedule.agents:
                sol_val = agent.current_step.get_best_sol_value()
                if(sol_val < best_sol_val):
                    best_sol = agent.current_step.get_best_sol()
                    best_sol_val = sol_val
            
            return best_sol_val

        self.datacollector = DataCollector(
            model_reporters={"TheGlobalBest": compute_global_best_state, "TheGlobalBestValue": compute_global_best_value},   
        )

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)