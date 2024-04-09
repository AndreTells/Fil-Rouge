from geneticAlgorithm import genetic_algorithm

from loadData import getData
import pandas as pd

truckKg = 20000
truckVol = 20


def main(route, popsize=100):
    # Get data from each frame
    customersDf = pd.read_excel("data/2_detail_table_customers.xls")
    depotsDf = pd.read_excel("data/4_detail_table_depots.xls")
    trucksDf = pd.read_excel("data/3_detail_table_vehicles.xlsx")
    routes = customersDf["ROUTE_ID"].unique()

    (numberOfTrucks, customers, cost, demandForAll) = getData(
        route, customersDf, depotsDf, trucksDf
    )
    best_solution, best_fitness, history = genetic_algorithm(
        popsize,
        numberOfTrucks,
        truckKg,
        truckVol,
        customers,
        cost,
        demandForAll,
        maxGenNumber=340,
        mutationRate=0.12,
    )


if __name__ == "__main__":
    main(2946091)
