import random

def standard_selection(population, fitness_scores):
  if(len(population) ==2):

    parents = [population[0], population[1]]
    population.pop(0)
    population.pop(0)
    return parents
  parents = []
  while len(parents) < 2 or population == []:
    tournament_size = max(len(population)//5,1)
    competitors = random.sample(population, tournament_size)
    competitor_scores = [fitness_scores[population.index(c)] for c in competitors]
    best_index = competitor_scores.index(max(competitor_scores))
    parents.append(competitors[best_index])
    population.pop(population.index(competitors[best_index]))

  if len(parents) == 1:
    parents.append(parents[0])
  return parents

