from mesa import Agent

class SolverAgent(Agent):
    def __init__(self,
                 unique_id,
                 model,
                 init_step,
                 step_function,
                 colaborative = False,
                 allow_worse_sols = False):
        super().__init__(unique_id, model)
        self.current_step = init_step
        self.step_function = step_function
        self.colaborative = colaborative
        self.allow_worse_sols = allow_worse_sols

    def share_step(self, step):
        model.solution_pool.add_solution(step)
        return

    def get_help(self):
        self.current_step = model.solution_pool.get_best_sol()
        if(self.current_step == None):
            self.current_step = model.rand_step_generator()      
        return
        

    def step(self):
        if(self.colaborative):
            self.get_help()

        new_step = self.step_function(self.current_step)

        if(new_step.get_best_sol_value()> self.current_step.get_best_sol_value()):    
            self.current_step = new_step if self.allow_worse_sols else self.current_step
        else:
            self.current_step = new_step

        if(self.colaborative):
            self.share_step(new_step)