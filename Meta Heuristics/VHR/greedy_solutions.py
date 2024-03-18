from .capacity import *

def nearest_neighbour_solution(graph, 
                    node_demand, 
                    capacity,
                    capacity_add = capacity_add,
                    capacity_null_value = capacity_null_value, 
                    capacity_condition = capacity_condition,
                    start_node = 1):
    num_of_nodes = len(graph)
    init_guess = [[0]]
    unexplored = [False] + [True for _ in range(num_of_nodes-1)]
    current_vehicle = 0
    current_node = start_node

    current_path_dist = 0
    current_load = capacity_null_value()
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
            current_path_dist = 0
            init_guess[current_vehicle].append(0)

        current_node = min_i
        current_path_dist += min_dist
        current_load = capacity_add(current_load, node_demand[min_i])

    res = sum(init_guess,[])
    res.append(0)
    return res[:-1]