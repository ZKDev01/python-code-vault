import random

def roll_dice(a: int, b: int):
  if not (isinstance(a, int) and isinstance(b, int)):
    raise Exception("Error con los parámetros")
  roll = random.randint(a, b)
  return roll

def simple_auto_roll_dice(funds, initial_wager, wager_count):
  value = funds
  wager = initial_wager

  current = 0

  def evaluate_random():
    result = roll_dice(a=1,b=5)
    return result == 5 or result == 4

  while current < wager_count:
    if evaluate_random():
      value += wager
    else:
      value -= wager
    
    current += 1

  return value


simple_auto_roll_dice(10, 10, 20)