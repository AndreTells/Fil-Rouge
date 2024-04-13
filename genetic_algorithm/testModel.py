from mesa import Model
from mesa.time import SimultaneousActivation
from mesa import DataCollector
import pandas as pd
from loadData import getData
from GeneticAgent import GeneticAgent


class modelTest(Model):
    def __init__(self, routeId):
        super().__init__()
        self.schedule = SimultaneousActivation(self)
        customersDf = pd.read_excel("data/2_detail_table_customers.xls")
        depotsDf = pd.read_excel("data/4_detail_table_depots.xls")
        trucksDf = pd.read_excel("data/3_detail_table_vehicles.xlsx")
        numberOfTrucks, customers, cost, demand = getData(
            routeId, customersDf, depotsDf, trucksDf
        )
        for i in range(2):
            agent = GeneticAgent(
                i, self, 100, numberOfTrucks, 20000, 20, customers, cost, demand
            )
            self.schedule.add(agent)
        self.datacollector = DataCollector(
            # model_reporters={"TheGlobalBest": compute_global_best},
            agent_reporters={"Best": lambda a: a.bestFitness}
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()


generations = 200

model = modelTest(2946091)

for i in range(generations):
    print(f"Génération n{i+1}")
    model.step()


agent_state = model.datacollector.get_agent_vars_dataframe()
print(agent_state)
res = agent_state.unstack()
print(res)
res.plot()
print("la meilleure valeur trouvée : ")
print(res.min().min())
