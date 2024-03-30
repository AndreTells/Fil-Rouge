# generic step for a solver
class SolverStep:
    def __init__(self, current_step, state, state_value, step_size):
        # history of execution of steps
        self.current_step = current_step
        # a solution to the problem in question
        self.state = state
        # the value of the solution above
        self.state_value = state_value
        # how many interations the next step will do
        self.step_size = step_size

    def get_step_count(self):
        return self.current_step

    def get_best_sol(self):
        return self.state

    def get_best_sol_value(self):
        return self.state_value

    def get_step_size(self):
        return self.step_size

    def set_step_size(self, new_step_size):
        self.step_size = new_step_size