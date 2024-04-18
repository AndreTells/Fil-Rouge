from typing import TypeVar, Generic
T = TypeVar("T")
# description of generic step for a solver
class SolverStep(Generic[T]):
    current_step: int
    state: T
    state_value: float
    step_size: int

    def __init__(self, state: T, state_value: float, step_size: int):
        # a solution to the problem in question
        self.state: T = state
        # the value of the solution above
        self.state_value = state_value
        # how many interations the next step will do
        self.step_size = step_size

    def get_best_sol(self)->T:
        return self.state

    def get_best_sol_value(self)->float:
        return self.state_value

    def get_step_size(self)->int:
        return self.step_size

    def set_step_size(self, new_step_size: int):
        self.step_size = new_step_size