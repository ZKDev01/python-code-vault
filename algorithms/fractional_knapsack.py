def fractional_knapsack(capacity, weights, values):
  "Resuelve el problema de la mochila fraccional usando algoritmo greedy"
  # calcular el valor por unidad de peso
  items = []
  for i in range(len(weights)):
    items.append((values[i]/weights[i], weights[i], values[i]))
  
  # ordenar por valor/peso descendente
  items.sort(reverse=True, key=lambda x: x[0])
  
  total_value = 0.0 
  remaining_capacity = capacity
  
  for ratio, weight, value in items:
    if remaining_capacity >= weight:
      # tomar el objeto completo
      total_value += value
      remaining_capacity -= weight
    else:
      # tomar fracción del objeto
      fraction = remaining_capacity / weight
      total_value += value * fraction
      break
  
  return total_value

if __name__ == "__main__":
  values =  [60, 100, 120]
  weights = [10,  20,  30]
  capacity = 50
  
  total_value = fractional_knapsack(capacity=capacity, weights=weights, values=values)
  print(f"Valor máximo en mochila: {total_value}")
