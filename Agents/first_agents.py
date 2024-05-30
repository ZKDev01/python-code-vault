from numpy.random import choice

""" 
vocales
"""
vowels = ['a', 'i']

"""
F = Flexible
S = Stubborn
"""
personalities = ['F', 'S']

def make_population_identical(n):
  n = []

def make_population(n):
  pass

def count(population, vowel = 'a'):
  t = 0.
  for item in population:
    if item[0] == vowel:
      t=t+1
  return t/len(population)

def choose_pair(population):
  i,j = [] # values
  return population[i], population[j]

def interact(listener, producer):
  pass

def simulate(n, k):
  population = make_population(n)
  proportion = []
  ## CODE
  return population, proportion

if __name__ == "__main__":
  population, proportion = simulate(n=10, k=5)
  result = f""" 
  Population: {population}
  Proportion: {proportion}
  """
