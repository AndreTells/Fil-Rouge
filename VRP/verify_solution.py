from collections.abc import Callable
from .capacity import *
Path = list[int]

def num_vehicles(path: Path)->int:
    return path.count(0)-1

# returns whether the given sequence of nodes breaks the capacity condition or the must visit every node condition
def valid_path(
    path: Path,
    capacity: Capacity,
    node_demand: list[Capacity],
    capacity_add: Callable[[Capacity,Capacity],Capacity] = capacity_add,
    capacity_null_value : Callable[[], Capacity]= capacity_null_value,
    capacity_condition:  Callable[[Capacity,Capacity],bool]= capacity_condition
    )->bool:
    
    visited_nodes = [x for x in path if x!=0]
    if(len(visited_nodes)+1 != len(node_demand)):
        return False

    path_load = capacity_null_value()
    for i in range(len(path)-1):
        current_node = path[i]
        next_node = path[i+1]

        if(current_node == 0):
            path_load = capacity_null_value()

        path_load = capacity_add(path_load, node_demand[current_node])
        if(not capacity_condition(path_load,capacity)):
            return False

    return True

# calculates the total distance of the path sol through the graph `mat`
def calculate_path_distance(sol:Path, mat: list[list[float]])-> float:
    value: float = 0
    for i,j in zip(sol[:-1], sol[1:]):
        value += mat[i][j]
    return value
