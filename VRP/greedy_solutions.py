from collections.abc import Callable
from .capacity import *
import random
Path = list[int]

# returns a solution to the VRP by always picking the clossest neighbour
def nearest_neighbour_solution(
                    graph: list[list[float]], 
                    node_demand: list[Capacity], 
                    capacity: Capacity,
                    capacity_add: Callable[[Capacity,Capacity],Capacity] = capacity_add,
                    capacity_null_value: Callable[[], Capacity] = capacity_null_value, 
                    capacity_condition: Callable[[Capacity,Capacity],bool] = capacity_condition,
                    start_node = 1)-> Path:
    num_of_nodes = len(graph)
    init_guess = [[0]]
    unexplored = [False] + [True for _ in range(num_of_nodes-1)]
    current_vehicle = 0
    current_node = start_node

    current_load = node_demand[current_node]
    while sum(unexplored) != 0:
        #print(current_capacity, current_node)
        
        unexplored[current_node] = False
        init_guess[current_vehicle].append(current_node)
        min_dist = float('inf')
        min_i = current_node
        for i in range(len(graph[current_node])):
            if((not unexplored[i]) or i == current_node):
                continue
            if(min_dist > graph[current_node][i]):
                min_dist = graph[current_node][i]
                min_i = i

        if ((not capacity_condition(capacity_add(current_load, node_demand[min_i]),capacity)) or min_i == current_node):
            init_guess.append([])
            current_vehicle += 1

            current_load = capacity_null_value()
            init_guess[current_vehicle].append(0)

        current_node = min_i
        current_load = capacity_add(current_load, node_demand[min_i])

    res = sum(init_guess,[])
    res.append(0)
    return res[:-1]

def random_solution(graph: list[list[float]], 
                    node_demand: list[Capacity], 
                    capacity: Capacity,
                    capacity_add: Callable[[Capacity,Capacity],Capacity] = capacity_add,
                    capacity_null_value: Callable[[], Capacity] = capacity_null_value, 
                    capacity_condition: Callable[[Capacity,Capacity],bool] = capacity_condition,
                    start_node = 1)-> Path:
    num_of_nodes = len(graph)
    init_guess = [[0]]
    unexplored = [False] + [True for _ in range(num_of_nodes-1)]
    current_vehicle = 0
    current_node = start_node

    current_load = node_demand[current_node]
    while sum(unexplored) != 0:
        #print(current_capacity, current_node)
        
        unexplored[current_node] = False
        init_guess[current_vehicle].append(current_node)
        
        rand_i = current_node    
        possible_nodes = [a for a in range(num_of_nodes) if unexplored[a]==True]
        if possible_nodes:
            rand_i = random.choice(possible_nodes)

        if ((not capacity_condition(capacity_add(current_load, node_demand[rand_i]),capacity)) or rand_i == current_node):
            init_guess.append([])
            current_vehicle += 1

            current_load = capacity_null_value()
            init_guess[current_vehicle].append(0)

        current_node = rand_i
        current_load = capacity_add(current_load, node_demand[rand_i])

    res = sum(init_guess,[])
    res.append(0)
    return res[:-1]