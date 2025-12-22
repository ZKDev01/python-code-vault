def max_coin_value(v):
  n = len(v) 
  
  if n == 0:
    return 0
  
  # 1. pre-calcular sumas acumulativas
  prefix = [0] * (n+1)
  prefix[0] = 0
  for i in range(1,n+1):
    prefix[i] = prefix[i-1] + v[i-1]
  
  # 2. inicializar la matriz M
  M = [[0]*n for _ in range(n)]
  for i in range(n):
    M[i][i] = v[i]
  
  # 3. llenar M 
  for l in range(2, n+1): 
    for i in range(0, n-l+1):
      j = i+l-1
      T = prefix[j+1] - prefix[i] 
      M[i][j] = T - min(M[i+1][j], M[i][j-1])
  
  # 4. solución
  return M[0][n-1]

if __name__ == "__main__": 
  array = [ 5,3,7,10,11,12,13,4,9,10,4,6,1,3,5,7,5,4,2,1 ]
  v_max = max_coin_value(array)
  print(f"{array} -> {v_max}")