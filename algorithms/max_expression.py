def max_expression(a, operators):
  n = len(a)
  min_val = [[0]*n for _ in range(n)]
  max_val = [[0]*n for _ in range(n)]
  
  for i in range(n):
    min_val[i][i] = max_val[i][i] = a[i]
    
  for L in range(2, n+1):
    for i in range(n-L+1):
      j = i+L-1
      min_val[i][j] = float('inf')
      max_val[i][j] = float('-inf')
            
      for k in range(i, j):
        pass
        # Combinar resultados izquierda y derecha
        # Actualizar min_val[i][j] y max_val[i][j]
    
  return max_val[0][n-1]