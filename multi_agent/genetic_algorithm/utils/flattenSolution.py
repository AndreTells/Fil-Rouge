def flattenSolution(solution):
    # Flattens the array to be in the format : 0,1,2,0,3,2,0,2,1,0
    flattenedArray = []
    for truck in solution[:-1]:  # Exclude last solution
        flattenedArray.extend(truck[:-1])  # Exclude trailing zero
    flattenedArray.extend(solution[-1])  # Include last solution
    return flattenedArray


def rebuildFlattenSolution(flattenSol):
    trucks = []
    truck = [0]
    for elem in flattenSol[1:]:  # Exclude start zero
        if elem == 0:
            truck.append(0)
            trucks.append(truck)
            truck = [0]
        else:
            truck.append(elem)
    return trucks
