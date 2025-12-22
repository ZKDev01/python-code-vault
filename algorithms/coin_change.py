from typing import List

def coin_change(coins:List[int], X:int) -> int:
  "Algoritmo para resolver el Coin Change Problem usando Programación Dinámica"
  # Inicializar DP 
  dp = [float('inf')] * (X+1)
  dp[0] = 0   # caso base
  
  # Calcular DP
  for i in range(1, X+1):
    for c in coins:
      if c <= i:
        dp[i] = min(dp[i], dp[i-c] + 1)
  
  return dp[X] if dp[X] != float('inf') else -1

if __name__ == "__main__":
  coins = [2,3,5,10,25,50]
  X = 123456789
  
  # solve
  change = coin_change(coins=coins, X=X)
  
  # show result
  print(f"X={X} (coins={coins}) => {change}")