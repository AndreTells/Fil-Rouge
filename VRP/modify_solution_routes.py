import random
import math
Path = list[int]

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