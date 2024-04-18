import random
import math
Path = list[int]

def combined_rand_modification(path, num_of_nodes, mat: list[list[float]])->Path:
    possible_neighbour_functions = [intra_route_swap,inter_route_swap,intra_route_shift,inter_route_shift,two_intra_route_shift,two_intra_route_swap,remove_smallest_route,remove_random_route,split_biggest_route,split_random_route]
    
    return random.choice(possible_neighbour_functions)(path, num_of_nodes, mat)

def intra_route_swap(path, num_of_nodes, mat: list[list[float]]):
    # split into routes
    path_list: list[Path]= []
    path_id = -1
    for i in path:
        if(i == 0):
            if(path_id != -1):
                path_list[path_id].append(i)
            
            path_list.append([])

            path_id+=1
        path_list[path_id].append(i)
    
    # picks random number
    random_path_id = int((len(path_list)-1) * random.random())
    # swaps two numbers
    if(len(path_list[random_path_id])-2 > 1):
        i = int((len(path_list[random_path_id])-2) * random.random()) + 1 # generate a random number between 1 and num_of_nodes
        j = int((len(path_list[random_path_id])-2) * random.random()) + 1 # generate a random number between 1 and num_of_nodes
        
        path_list[random_path_id][i], path_list[random_path_id][j] = path_list[random_path_id][j], path_list[random_path_id][i]
   
    # join paths
    return sum([x[:-1] for x in path_list],[])+[0]

def inter_route_swap(path, num_of_nodes, mat: list[list[float]]):
    # split into routes
    path_list: list[Path]= []
    path_id = -1
    for i in path:
        if(i == 0):
            if(path_id != -1):
                path_list[path_id].append(i)
            
            path_list.append([])

            path_id+=1
        path_list[path_id].append(i)
   
    if(len(path_list)-1 <2):
        return path

    # picks two random lists
    random_path_id_1 = int((len(path_list)-1) * random.random())
    random_path_id_2 = int((len(path_list)-1) * random.random())
    # swaps two numbers 
    i = int((len(path_list[random_path_id_1])-2) * random.random()) + 1 # generate a random number between 1 and num_of_nodes
    j = int((len(path_list[random_path_id_2])-2) * random.random()) + 1 # generate a random number between 1 and num_of_nodes

    path_list[random_path_id_1][i], path_list[random_path_id_2][j] = path_list[random_path_id_2][j], path_list[random_path_id_1][i]
   
    # joins paths
    return sum([x[:-1] for x in path_list],[])+[0]

def intra_route_shift(path, num_of_nodes, mat: list[list[float]]):
    # split into routes
    path_list: list[Path]= []
    path_id = -1
    for i in path:
        if(i == 0):
            if(path_id != -1):
                path_list[path_id].append(i)
            
            path_list.append([])

            path_id+=1
        path_list[path_id].append(i)
    
    # picks random number
    random_path_id = int((len(path_list)-1) * random.random())
    # shifts one numbers
    if(len(path_list[random_path_id])-2 > 1):
        i = int((len(path_list[random_path_id])-2) * random.random()) + 1 # generate a random number between 1 and num_of_nodes
        popped_node = path_list[random_path_id].pop(i)
        
        j = int((len(path_list[random_path_id])-2) * random.random()) + 1 # generate a random number between 1 and num_of_nodes
        path_list[random_path_id].insert(j, popped_node)
   
    # join paths
    return sum([x[:-1] for x in path_list],[])+[0]

def inter_route_shift(path, num_of_nodes, mat: list[list[float]]):
    # split into routes
    path_list: list[Path]= []
    path_id = -1
    for i in path:
        if(i == 0):
            if(path_id != -1):
                path_list[path_id].append(i)
            
            path_list.append([])

            path_id+=1
        path_list[path_id].append(i)
    
    # picks random number
    random_path_id_1 = int((len(path_list)-1) * random.random())
    random_path_id_2 = int((len(path_list)-1) * random.random())

    # shift one number
    if(len(path_list[random_path_id_1])-2 > 1):
        i = int((len(path_list[random_path_id_1])-2) * random.random()) + 1 # generate a random number between 1 and num_of_nodes
        popped_node = path_list[random_path_id_1].pop(i)
        
        j = int((len(path_list[random_path_id_2])-2) * random.random()) + 1 # generate a random number between 1 and num_of_nodes
        path_list[random_path_id_2].insert(j, popped_node)

    # join paths
    return sum([x[:-1] for x in path_list],[])+[0]

def two_intra_route_shift(path, num_of_nodes, mat: list[list[float]]):
    # split into routes
    path_list: list[Path]= []
    path_id = -1
    for i in path:
        if(i == 0):
            if(path_id != -1):
                path_list[path_id].append(i)
            
            path_list.append([])

            path_id+=1
        path_list[path_id].append(i)
    
    # picks random number
    random_path_id = int((len(path_list)-1) * random.random())
    # shifts one numbers
    if(len(path_list[random_path_id])-2 > 2):
        i = int((len(path_list[random_path_id])-3) * random.random()) + 1 # generate a random number between 1 and num_of_nodes
        popped_node_1 = path_list[random_path_id].pop(i)
        popped_node_2 = path_list[random_path_id].pop(i)
        

        j = int((len(path_list[random_path_id])-2) * random.random()) + 1 # generate a random number between 1 and num_of_nodes
        path_list[random_path_id].insert(j, popped_node_2)
        path_list[random_path_id].insert(j, popped_node_1)
   
    # join paths
    return sum([x[:-1] for x in path_list],[])+[0]

def two_intra_route_swap(path, num_of_nodes, mat: list[list[float]]):
    # split into routes
    path_list: list[Path]= []
    path_id = -1
    for i in path:
        if(i == 0):
            if(path_id != -1):
                path_list[path_id].append(i)
            
            path_list.append([])

            path_id+=1
        path_list[path_id].append(i)
    
    # picks random number
    random_path_id = int((len(path_list)-1) * random.random())
    # swaps two numbers
    if(len(path_list[random_path_id])-2 > 5):
        i = int((len(path_list[random_path_id])-3) * random.random()) + 1 # generate a random number between 1 and num_of_nodes
        
        j = random.choice( [k for k in range(1,len(path_list[random_path_id])-2) if (k!=i and k!=i+1 and k!=i-1)])
        path_list[random_path_id][i],path_list[random_path_id][i+1], path_list[random_path_id][j],path_list[random_path_id][j+1] = path_list[random_path_id][j], path_list[random_path_id][j+1], path_list[random_path_id][i], path_list[random_path_id][i+1]
   
    # join paths
    return sum([x[:-1] for x in path_list],[])+[0]

def remove_smallest_route(path: Path, num_of_nodes: int, mat: list[list[float]]):
    path_list: list[Path]= []
    path_id = -1

    smallest_path_id = -1
    smallest_path_len = float('inf')


    current_path_len = 0
    for i in path:
        if(i == 0):
            if(path_id != -1):
                path_list[path_id].append(i)
                if(current_path_len<smallest_path_len):
                    smallest_path_id = path_id
                    smallest_path_len = current_path_len
            
            path_list.append([])
            current_path_len = 0

            path_id+=1

        path_list[path_id].append(i)
        if(len(path_list[path_id])<=2):
            continue
        current_path_len +=mat[path_list[path_id][-2]][i]
        
    if(len(path_list) == 2):
        return path

    init_pos = sum([len(x[:-1]) for x in path_list[:smallest_path_id]])
    end_pos = sum([len(x[:-1]) for x in path_list[:smallest_path_id+1]])

    new_path = path[:init_pos] + path[end_pos:]
    for i in path_list[smallest_path_id][1:-1]:
        nearest_node = -1 
        smallest_dist = float('inf')

        for j in new_path:
            if(mat[i][j]<smallest_dist):
                nearest_node = j
                smallest_dist = mat[i][j]

        index_nearest_node = new_path.index(nearest_node)
        new_path.insert(index_nearest_node+1,i)

    return new_path

def remove_random_route(path: Path, num_of_nodes: int, mat: list[list[float]]):
    path_list: list[Path]= []
    path_id = -1
    for i in path:
        if(i == 0):
            if(path_id != -1):
                path_list[path_id].append(i)
            
            path_list.append([])

            path_id+=1
        path_list[path_id].append(i)

    if(len(path_list) == 2):
        return path

    random_path_id = int((len(path_list)-1) * random.random())

    init_pos = sum([len(x[:-1]) for x in path_list[:random_path_id]])
    end_pos = sum([len(x[:-1]) for x in path_list[:random_path_id+1]])

    new_path = path[:init_pos] + path[end_pos:]
    for i in path_list[random_path_id][1:-1]:
        nearest_node = -1 
        smallest_dist = float('inf')

        for j in new_path:
            if(mat[i][j]<smallest_dist):
                nearest_node = j
                smallest_dist = mat[i][j]

        index_nearest_node = new_path.index(nearest_node)
        new_path.insert(index_nearest_node+1,i)

    return new_path

def split_biggest_route(path: Path, num_of_nodes: int, mat: list[list[float]]):
    path_list: list[Path]= []
    path_id = -1

    biggest_path_id = -1
    biggest_path_len = -float('inf')
    
    current_path_len = 0
    for i in path:
        if(i == 0):
            if(path_id != -1):
                path_list[path_id].append(i)
                if(current_path_len>biggest_path_len):
                    biggest_path_id = path_id
                    biggest_path_len = current_path_len
            
            path_list.append([])
            current_path_len = 0

            path_id+=1

        path_list[path_id].append(i)
        if(len(path_list[path_id])<=2):
            continue
        current_path_len +=mat[path_list[path_id][-2]][i]
        
    list_len = len(path_list[biggest_path_id])
    if(list_len ==3):
        return path
    init_pos = sum([len(x[:-1]) for x in path_list[:biggest_path_id]])
    end_pos = sum([len(x[:-1]) for x in path_list[:biggest_path_id+1]])

    new_path = path[:init_pos+(list_len//2)]+ [0] + path[1-(list_len-list_len//2)+end_pos:]
    
    return new_path

def split_random_route(path: Path, num_of_nodes: int, mat: list[list[float]]):
    path_list: list[Path]= []
    path_id = -1
    for i in path:
        if(i == 0):
            if(path_id != -1):
                path_list[path_id].append(i)
            
            path_list.append([])

            path_id+=1
        path_list[path_id].append(i)

    random_path_id = int((len(path_list)-1) * random.random())

    list_len = len(path_list[random_path_id])
    if(list_len ==3):
        return path
    init_pos = sum([len(x[:-1]) for x in path_list[:random_path_id]])
    end_pos = sum([len(x[:-1]) for x in path_list[:random_path_id+1]])


    new_path = path[:init_pos+(list_len//2)]+ [0] + path[1-(list_len-list_len//2)+end_pos:]
    
    return new_path
