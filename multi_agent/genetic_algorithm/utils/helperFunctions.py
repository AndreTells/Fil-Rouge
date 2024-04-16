def canAddCustomerToTruck(
    truck, truckCapacityKg, truckCapacityVol, singleDemand, allCustomersDemands
):
    """This function just checks if it's possible to add the delivery of someone into a truck"""
    total_weight = (
        sum(allCustomersDemands[customer][0] for customer in truck if customer != 0)
        + singleDemand[0]
    )
    total_volume = (
        sum(allCustomersDemands[customer][1] for customer in truck if customer != 0)
        + singleDemand[1]
    )
    return total_weight <= truckCapacityKg and total_volume <= truckCapacityVol


def calculate_route_cost(route, cost):
    """This function calculates total route cost in terms of time"""
    totalCost = 0
    for i in range(len(route) - 1):
        edge = (route[i], route[i + 1])
        totalCost += cost[edge]
    return totalCost


def fitnessFunction(solution, cost):
    """Returns total cost of a solution"""
    totalCost = 0
    for route in solution:
        if route == [0, 0]:
            continue
        totalCost += calculate_route_cost(route, cost)
    return totalCost


def flatten(routes):
    return [node for route in routes for node in route[1:-1]]  # Not interested in the 0
