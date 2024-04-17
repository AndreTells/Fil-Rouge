import random
from dataclasses import dataclass

def init_q_learning_table(q_size):
    return [[ 0 for _ in range(q_size)] for _ in range(q_size)]

@dataclass(init=True)
class q_learning_obj:
    q_state: int
    q_table: list[list[float]]
    q_size: int
    discount_rate: float
    learning_rate: float

def epsilon_greedy(epsilon, q):
    p = random.random()
    if(p<=epsilon):
        return min(int(random.random()*(q.q_size)),q.q_size)
    else:
        return q.q_table[q.q_state].index(max(q.q_table[q.q_state]))

def q_learning_iteration(path,q, neighbour_function_list, eval_function ,epsilon = 0.8):
    new_action = epsilon_greedy(epsilon, q)
    new_state = neighbour_function_list[new_action](path)
    r = eval_function(new_state) - eval_function(new_state)

    q.q_table[q.q_state][new_action] = ((1-q.learning_rate)*q.q_table[q.q_state][new_action]) + (q.learning_rate*(r+(q.discount_rate*max(q.q_table[q.q_state]))))
    q.q_state = new_action
    
    return new_state