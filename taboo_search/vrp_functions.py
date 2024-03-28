from random import uniform

def _split_paths(paths):
    path_list= []
    path_id = -1
    for i in paths:
        if(i == 0):
            if(path_id != -1):
                path_list[path_id].append(i)    
            path_list.append([])
            path_id+=1
        path_list[path_id].append(i)
        


    return path_list[:-1]

def _standard_capacity_add(a,b):
    return ((a[0]+b[0],a[1]+b[1],a[2]+b[2]))

def _standard_capacity_null_value():
    return (0,0,0)

def _standard_capacity_condition(current_load,capacity, node, current_path_dist, delivery_window_list):
    if(current_load[0]>= capacity[0] or current_load[1]>= capacity[1]):
        return False
    
    if(not(delivery_window_list[node][0]<= (current_load[2]+current_path_dist/10) and delivery_window_list[node][1]>= (current_load[2]+current_path_dist/10))):
        return False
    
    return True

def _standard_init_function(graph, node_demand, capacity,
                    capacity_add ,
                    capacity_null_value, 
                    capacity_condition):
    num_of_nodes = len(graph)
    init_guess = [[]]
    unexplored = [True for _ in range(num_of_nodes)]
    current_vehicle = 0
    current_node = 0

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

        if ((not capacity_condition(capacity_add(current_load, node_demand[min_i]),capacity, min_i, current_path_dist)) or min_i == current_node):
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

def _standard_state_to_energy(state,
                      graph, node_demand, capacity,
                      capacity_add,
                      capacity_null_value, 
                      capacity_condition):

    paths = _split_paths(state)
    for path in paths:

        path_load = capacity_null_value()
        path_dist = 0
        for i in range(1,len(path)):
            past_node = path[i-1]
            current_node = path[i]
            path_load = capacity_add(path_load, node_demand[current_node])
            path_dist += graph[current_node][past_node]
            if(not capacity_condition(path_load,capacity, current_node, path_dist)):
                return float('inf')
            
    total_cost = 0
    for i,j in zip(state[:-1],state[1:]):
        total_cost+=graph[i][j]
    
    return total_cost

def _get_neighbour_reverse_section(state, graph):
    num_of_nodes = len(graph)
    i = int(uniform(1,num_of_nodes))
    j = min(i + int(uniform(1,10)),num_of_nodes)
    new_state = state.copy()
    state_slice = list(reversed(new_state[i:j]))
    new_state = new_state[:i]+ state_slice+ new_state[j:]

    return new_state

def _get_neighbour_opt_n(state, graph, n=3):
    num_of_nodes = len(graph)
    new_state = state.copy()
    for K in range(n):
        i = int(uniform(1,num_of_nodes))
        j = int(uniform(1,num_of_nodes))
        new_state[i], new_state[j] = new_state[j], new_state[i]
    return new_state

def _standard_get_neighbour(state, graph):
    decider = uniform(0,1)
    if(decider >=0.5):
        return _get_neighbour_opt_n(state,graph, n=1)

    return _get_neighbour_reverse_section(state,graph)

vrp_function_config = {
    'standard':{
        'capacity_add': _standard_capacity_add,
        'capacity_null_value': _standard_capacity_null_value,
        'capacity_condition': _standard_capacity_condition,
        'init_function': _standard_init_function,
        'state_to_energy': _standard_state_to_energy,
        'get_neighbour': _standard_get_neighbour
    }
}
