from .capacity import *


# returns whether the given sequence of nodes breaks the capacity condition
def valid_path(
    path,
    capacity,
    node_demand,
    capacity_add = capacity_add,
    capacity_null_value = capacity_null_value,
    capacity_condition = capacity_condition
    ):

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
def calculate_path_distance(sol, mat):
    value = 0
    for i,j in zip(sol[:-1], sol[1:]):
        value += mat[i][j]
    return value
