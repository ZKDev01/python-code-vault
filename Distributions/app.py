import numpy as np
import matplotlib.pyplot as plt

# uniform distribution 
def show_uniform():
  uniform = np.random.uniform(0, 6, size=1000)

  fig, aux = plt.subplots()
  plt.hist(uniform, density=True, bins=6)
  plt.title('Uniform Distribution', size=14)
  plt.xlabel('Samples')
  plt.ylabel('Density')
  plt.axhline(1/6, color='blue', linestyle='--')

  return uniform, plt.show

# binomial distribution 
def show_binomial():
  binomial = np.random.binomial(10, 0.5, size=10000)

  fig, aux = plt.subplots()
  plt.hist(binomial, density=True, bins=11)
  plt.title('Binomial Distribution', size=14)
  plt.xlabel('Samples')
  plt.ylabel('Density')
  plt.axhline(10*0.5, color='blue', linestyle='--')
  plt.axhline(0, color='red', linestyle='--')
  plt.axhline(10, color='#3793ef', linestyle='--')
  
  return binomial, plt.show

# poisson distribution 
def show_poisson():
  poisson = np.random.poisson(3, 10000)

  fig, ax = plt.subplots()
  plt.hist(poisson, density=True, bins=10)
  plt.title('Poisson Distribution', size=14)
  plt.xlabel('Samples')
  plt.ylabel('Density')
  plt.axvline(3, color='#3793ef', linestyle='--')
  
  return poisson, plt.show

# exponential distribution
def show_exponential():
  exponential = np.random.exponential(3, 10000)

  fig, ax = plt.subplots()
  plt.hist(exponential, density=True, bins=1000)
  plt.title('Exponential Distribution', size=14)
  plt.xlabel('Samples')
  plt.ylabel('Density')
  
  return exponential, plt.show

# normal distribution
def show_normal():
  normal = np.random.normal(0, 1, size=10000)

  fig, ax = plt.subplots()
  plt.hist(normal, density=True, bins=50)
  plt.title('Normal Distribution', size=14)
  plt.xlabel('Samples')
  plt.ylabel('Density')
  plt.axvline(0, color='#3793ef', linestyle='--')
  plt.axvline(np.std(normal), color='#3793ef', linestyle='--')
  plt.axvline(-1*np.std(normal), color='#3793ef', linestyle='--')
  
  return normal, plt.show

# cumulative distribution function
def show_ecdf(distribution):
  n = len(distribution)
  x = np.sort(distribution)
  y = np.arange(1, n+1) / n

  fig, ax = plt.subplots()
  plt.plot(x, y)
  plt.title('ECDF', size=14)
  plt.xlabel('Samples')
  plt.ylabel('Cumulative')
  plt.axvline(0, color='#3793ef', linestyle='--')
  plt.axhline(0.5, color='#3793ef', linestyle='--')
  
  return plt.show

distribution, show = show_normal()
show()
show = show_ecdf(distribution)
show()