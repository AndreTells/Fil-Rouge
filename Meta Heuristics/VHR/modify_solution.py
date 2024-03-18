import random

def rand_opt_n(path, num_of_nodes, n=1):
    new_state = path[:] # fastest way to copy a list in python
    for k in range(n):
        i = int((num_of_nodes-1) * random.random()) + 1 # generate a random number between 1 and num_of_nodes
        j = int((num_of_nodes-1) * random.random()) + 1 # generate a random number between 1 and num_of_nodes

        new_state[i], new_state[j] = new_state[j], new_state[i]

    return new_state

def rand_reverse_section(path, num_of_nodes):
    i = int((num_of_nodes-1) * random.random()) + 1 # generate a random number between 1 and num_of_nodes
    j = min(i + int((num_of_nodes-1) * random.random()) + 1, num_of_nodes)# generate a random number between 1 and num_of_nodes

    path_slice = list(reversed(path[i:j]))
    new_path = path[:i]+ path_slice+ path[j:]

    return new_path

def combined_rand_modification(path, num_of_nodes):
    decider = random.random()
    if(decider >=0.5):
        return rand_opt_n(path,num_of_nodes)

    return rand_reverse_section(path, num_of_nodes)

def crossover_sols(path1,path2):
    crossover_point = int((len(path1)-3) * random.random()) + 1
    child1 = path1[:crossover_point] + path2[crossover_point:]
    child2 = path2[:crossover_point] + path1[crossover_point:]
    
    # Ensure no duplicates in child (important for TSP)
    for i in range(len(child1)):
        if child1[i] not in child1[:i]:
            continue
        for j in range(len(path2)):
            if child1[i] == path2[j] and j > crossover_point:
                child1[i] = path1[ (i + 1) % len(path1)]
                break
    for i in range(len(child2)):
        if child2[i] not in child2[:i]:
            continue
        for j in range(len(path1)):
            if child2[i] == path1[j] and j > crossover_point:
                child2[i] = path2[ (i + 1) % len(path2)]
                break

    return child1, child2