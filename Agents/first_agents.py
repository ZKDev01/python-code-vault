import random

""" 
vocales
"""
vowels = ['a', 'i']

"""
F = Flexible
S = Stubborn
"""
personalities = ['F', 'S']

def make_population_identical(n, index_vowel, index_personality):
  population_identical = []
  for _ in range(n):
    pair = [vowels[index_vowel],personalities[index_personality]]
    population_identical.append(pair)
  return population_identical

def make_population(n):
  population = []
  for _ in range(n):
    index_x = random.choice(range(len(vowels)))
    index_y = random.choice(range(len(personalities)))
    pair = [vowels[index_x],personalities[index_y]]
    population.append(pair)
  return population

def count(population, vowel = 'a'):
  t = 0.
  for item in population:
    if item[0] == vowel:
      t=t+1
  return t/len(population)

def choose_pair(population):
  i = random.choice(range(len(population)))
  j = random.choice(range(len(population))) 
  if i == j:
    return choose_pair(population)
  return population[i], population[j]

"""
Si los agentes tienen vocales diferentes, entonces la acción del oyente depende 
de su personalidad previa: si son tercos, no cambiarán su vocal; pero si son flexibles, 
actualizarán su vocal según la del productor.

Entonces, si el oyente es flexible y tiene una variante diferente al productor, 
queremos actualizar la vocal del oyente según la vocal del productor.

Para hacer esto recuerde que los agentes son listas y por tanto mutables.
"""

def interact(listener, producer):
  if producer[0] == listener[0]:
    return listener, producer
  else: 
    action = listener[1]
    pass

def simulate(n, k):
  population = make_population(n)
  proportion = []

  for _ in range(k):
    listener, producer = choose_pair(population)
    interact(listener, producer)

  return population, proportion

def execute_result():
  population, proportion = simulate(n=10, k=5)
  result = f""" 
  Population: {population}
  Proportion: {proportion}
  """
  print(result)

if __name__ == "__main__":
  execute_result()
