def rod_cutting(L, values):
  dp = [0]*(L+1)
  cuts = [0]*(L+1)
  
  for i in range(1,L+1):
    v_max = float('-inf')
    for j in range(1,i+1):
      if values[j] + dp[i-j] > v_max:
        v_max = values[j] + dp[i-j]
        cuts[i] = j   # guardar el corte que maximiza el valor 
    dp[i] = v_max
  
  optimal = []
  remaining = L
  while remaining > 0:
    cut_L = cuts[remaining]
    optimal.append(cut_L)
    remaining = remaining - cut_L
  
  return dp[L], optimal

if __name__ == "__main__":
  L = 7
  values = [0,1,10,13,18,20,31,32]
  
  v_max, cuts = rod_cutting(L, values)
  if sum(cuts) == L:
    print(f" Longitud de vara: L={L}")
    print(f" Valores por longitud: values={values}")
    print(f" Valor máximo: {v_max}")
    print(f" Cortes óptimos: {cuts}")