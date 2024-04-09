import random

from .helperFunctions import *

# General constant variables
truckKg = 2e4
truckVol = 20
truckSpd = 0.6


def initializePopulation(population_size, numberOfTrucks, customers, demandForCustomer):
    """This function just initializes and returns a starting population array while keeping the constraints in mind"""
    population = []
    random.seed()

    # Keeps increasing population
    for i in range(population_size):
        trucks = [[0] for _ in range(numberOfTrucks)]
        remainingCustomers = set(customers)

        # While there are customers remaining, try to assign them to a truck
        while remainingCustomers:
            for truck in trucks:
                # Early break to avoid unnecessary iteration
                if not remainingCustomers:
                    break

                # Choose a customer at random and see if its demand fits
                customerChosen = random.choice(list(remainingCustomers))
                demand = demandForCustomer[customerChosen]

                # If it does, add it to the truck and remove it from the remainingCustomers set.
                if canAddCustomerToTruck(
                    truck, truckKg, truckVol, demand, demandForCustomer
                ):
                    truck.append(customerChosen)
                    remainingCustomers.remove(customerChosen)
        # Add 0 at the end -> go home to depot:
        for truck in trucks:
            if len(truck) > 1:  # If it has at least one customer
                truck.append(0)

        population.append(trucks)

    return population
