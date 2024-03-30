from mesa import Agent

class VRPSolverAgent(Agent):
    def __init__(self,
                 unique_id,
                 model,
                 init_step,
                 step_function,
                 colaborative = False):
        super().__init__(unique_id, model)
        self.current_step = init_step
        self.step_function = step_function
        self.colaborative = colaborative

    def contact(self):
        # get best solution amongst agents
        # integrate best solution into current step
        pass
        

    def step(self):
        self.current_step = self.step_function(self.current_step)
        if(self.colaborative):
            self.contact()