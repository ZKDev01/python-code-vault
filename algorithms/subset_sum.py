def subset_sum(array, T):
  n = len(array)
  dp = [[False] * (T + 1) for _ in range(n + 1)]

  # caso base: suma 0 es siempre posible
  for i in range(0, n + 1):
    dp[i][0] = True

  # caso recursivo: llenar tabla dp
  for i in range(1, n + 1):
    for j in range(1, T + 1):
      if j < array[i - 1]:
        dp[i][j] = dp[i - 1][j]
      else:
        dp[i][j] = dp[i - 1][j] or dp[i - 1][j - array[i - 1]]

  # reconstruir el subconjunto
  subset = []
  i = n
  j = T
  if dp[n][T]:
    while i > 0 and j > 0:
      # si el elemento no fue incluido
      if dp[i - 1][j]:
        i -= 1
      else:
        # el elemento fue incluido
        subset.append(array[i - 1])
        j -= array[i - 1]
        i -= 1

  return dp[n][T], subset


def subset_sum_optimized(array, T):
  dp = [False] * (T + 1)
  dp[0] = True  # subconjunto vacío: suma 0

  for ai in array:
    # iterar hacia atrás para evitar reutilizar el mismo elemento
    for j in range(T, ai - 1, -1):
      if dp[j - ai]:
        dp[j] = True

  return dp[T]


if __name__ == "__main__":
  A = [1, 3, 4, 12, 19, 21, 22]
  T = 23
  decision, subset = subset_sum(A, T)
  if decision:
    print(f"Subset: {subset}")
