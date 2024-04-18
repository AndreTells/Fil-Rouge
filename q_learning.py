import random
from dataclasses import dataclass

# initializes a square matrix of size q_size with 0s
def init_q_learning_table(q_size):
    return [[ 0 for _ in range(q_size)] for _ in range(q_size)]

#class to store all the hyperparameters used by the q_learning algorithm
@dataclass(init=True)
class q_learning_obj:
    q_state: int
    q_table: list[list[float]]
    q_size: int
    discount_rate: float
    learning_rate: float

# action chosing policy that takes the best possible action predicted by the qtable epsilon % of the time
# and a random action the remaining 
def epsilon_greedy(epsilon, q):
    p = random.random()
    if(p<=epsilon):
        return min(int(random.random()*(q.q_size)),q.q_size)
    else:
        return q.q_table[q.q_state].index(max(q.q_table[q.q_state]))

# executes one iteration based on a description of the environent (path) and the
# current q state and hyperparameters(q) It also requires a way to may the action in the table, in other
# words index indexes, into actual actions so a function list is given (neighbour_function_list)
def q_learning_iteration(path,q, neighbour_function_list, eval_function ,epsilon = 0.8):
    new_action = epsilon_greedy(epsilon, q)
    new_state = neighbour_function_list[new_action](path)
    r = eval_function(new_state) - eval_function(new_state)

    q.q_table[q.q_state][new_action] = ((1-q.learning_rate)*q.q_table[q.q_state][new_action]) + (q.learning_rate*(r+(q.discount_rate*max(q.q_table[q.q_state]))))
    q.q_state = new_action
    
    return new_state