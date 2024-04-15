import pandas as pd
import numpy as np

# General constant variables
# truckKg = 2e4
# truckVol = 20
truckSpd = 0.6


def getCostDict(customers, depot, edges):
    """This function returns a cost dict"""
    cost = {}
    depot_lat, depot_lon = (
        depot.loc[0, "DEPOT_LATITUDE"],
        depot.loc[0, "DEPOT_LONGITUDE"],
    )
    for loc1, loc2 in edges:
        # Depot
        if loc1 == 0:
            cost[(loc1, loc2)] = round(
                np.hypot(
                    depot_lat - customers.loc[loc2, "CUSTOMER_LATITUDE"],
                    depot_lon - customers.loc[loc2, "CUSTOMER_LONGITUDE"],
                )
                / truckSpd,
                4,
            )
        elif loc2 == 0:
            cost[(loc1, loc2)] = round(
                np.hypot(
                    depot_lat - customers.loc[loc1, "CUSTOMER_LATITUDE"],
                    depot_lon - customers.loc[loc1, "CUSTOMER_LONGITUDE"],
                )
                / truckSpd,
                4,
            )
        else:
            cost[(loc1, loc2)] = round(
                np.hypot(
                    customers.loc[loc1, "CUSTOMER_LATITUDE"]
                    - customers.loc[loc2, "CUSTOMER_LATITUDE"],
                    customers.loc[loc1, "CUSTOMER_LONGITUDE"]
                    - customers.loc[loc2, "CUSTOMER_LONGITUDE"],
                )
                / truckSpd,
                4,
            )
    return cost


def getData(route, customersDf, depotsDf, trucksDf):
    """Returns Number of Trucks, List of Customers, Cost, Demand For all Customers"""
    C_df = (
        customersDf[customersDf["ROUTE_ID"] == route]
        .set_index("CUSTOMER_NUMBER", drop=False)
        .copy()
    )
    D_df = depotsDf[depotsDf["ROUTE_ID"] == route].reset_index()

    # Grabbing the amount of trucks available for each route
    numberOfTrucks = trucksDf[trucksDf["ROUTE_ID"] == route]["VEHICLE_NUMBER"].max()

    # truckCapacityKg = 20000
    # truckCapacityVolume = 10

    # Getting id for each customer and then adding the starting node (depot). this will be used to calculate distance
    customersId = list(C_df["CUSTOMER_NUMBER"].unique())
    V = [0] + customersId

    # Those represent the edges
    edges = [(i, j) for i in V for j in V if i != j]

    # This function gives back a dictionary that represents an edge from i to j, keys of the dictionary, and its value is the cost (time taken to travel from i to j)
    cost = getCostDict(C_df, D_df, edges)
    # This represents the demand of each customer i = (weight, volume)
    demandForCustomer = {
        i: (C_df.loc[i, "TOTAL_WEIGHT_KG"], C_df.loc[i, "TOTAL_VOLUME_M3"])
        for i in C_df.index.to_list()
    }
    return (numberOfTrucks, customersId, cost, demandForCustomer)
