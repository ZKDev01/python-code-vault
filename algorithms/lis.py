def lis_dynamic(sequence):
  # encuentra la subsecuencia creciente más larga (LIS) en una secuencia dada
  n = len(sequence)
  if n == 0:
    return 0, []
  
  L = [ 1]*n  # L[i] almacena la longitud de LIS que termina en sequence[i]
  p = [-1]*n  # p[i] almacena el índice del elemento anterior en la LIS
  
  # calcular LIS para cada posición
  for i in range(n):
    for j in range(i):
      if sequence[j] < sequence[i] and L[j] + 1 > L[i]:
        L[i] = L[j] + 1
        p[i] = j 
  
  # encontrar la máxima longitud y su posición final
  max_length = max(L)
  end_index = L.index(max_length)
  
  # reconstruir la longitud LIS
  LIS_sequence = []
  current = end_index
  while current != -1:
    LIS_sequence.append(sequence[current])
    current = p[current]
  
  LIS_sequence.reverse()
  return max_length, ''.join(LIS_sequence)

def lis_nlogn(sequence):
  pass 

def tests():
  pass 


if __name__ == "__main__":
  print(lis_dynamic("carbohydrate"))
  print(lis_dynamic("123456789"))
  print(lis_dynamic("987654321"))

