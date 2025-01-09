import random
import numpy as np  
import matplotlib.pyplot as plt

from scipy import stats
from typing import List, Tuple



def calculate_expected_value(outcomes, probabilities):
  return sum(outcome * probability for outcome, probability in zip(outcomes, probabilities))

def calculate_variance(outcomes, probabilities):
  expected_value = calculate_expected_value(outcomes, probabilities)
  return sum(probability * (outcome - expected_value) ** 2 for outcome, probability in zip(outcomes, probabilities))

def calculate_probability_of_event(event_outcomes, total_outcomes):
  return len(event_outcomes) / total_outcomes if total_outcomes > 0 else 0

def simulate_dice_rolls(num_rolls, sides=6):
  rolls = [random.randint(1, sides) for _ in range(num_rolls)]
  return rolls

def analyze_rolls(rolls):
  outcomes = range(1, 7)
  probabilities = [rolls.count(outcome) / len(rolls) for outcome in outcomes]
  expected_value = calculate_expected_value(outcomes, probabilities)
  variance = calculate_variance(outcomes, probabilities)
  return expected_value, variance, probabilities


def calculate_mean(data):
  return np.mean(data)

def calculate_standard_deviation(data):
  return np.std(data)

def generate_histogram(data, bins=10):
  plt.hist(data, bins=bins, alpha=0.7, color='blue')
  plt.title('Histogram of Simulation Results')
  plt.xlabel('Outcome')
  plt.ylabel('Frequency')
  plt.grid(True)
  plt.show()

def perform_t_test(data1, data2):
  t_statistic, p_value = stats.ttest_ind(data1, data2)
  return t_statistic, p_value

def confidence_interval(data, confidence=0.95):
  mean = calculate_mean(data)
  std_dev = calculate_standard_deviation(data)
  n = len(data)
  h = std_dev * stats.t.ppf((1 + confidence) / 2, n - 1) / np.sqrt(n)
  return mean - h, mean + h


def roll_dice(a: int, b: int) -> int:
  if not (isinstance(a, int) and isinstance(b, int)):
    raise ValueError("Invalid parameters: a and b must be integers.")
  return random.randint(a, b)

def simulate_dice_rolls(num_rolls: int, a: int = 1, b: int = 6) -> List[int]:
  results = [roll_dice(a, b) for _ in range(num_rolls)]
  return results

def analyze_rolls(rolls: List[int]) -> Tuple[float, float, float]:
  mean = sum(rolls) / len(rolls)
  variance = sum((x - mean) ** 2 for x in rolls) / len(rolls)
  return mean, variance, len(rolls)

def monte_carlo_simulation(num_simulations: int, num_rolls: int) -> List[Tuple[float, float, float]]:
  results = []
  for _ in range(num_simulations):
    rolls = simulate_dice_rolls(num_rolls)
    analysis = analyze_rolls(rolls)
    results.append(analysis)
  return results
