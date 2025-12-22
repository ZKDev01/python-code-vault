def git_diff_using_lcs_dynamic_cbc(s1, s2):
  # implementación char for char

  L, _, _ = lcs_dp(s1, s2)
  m, n = len(s1), len(s2)
  # reconstruir diff
  i, j = m, n
  diff = []

  while i > 0 or j > 0:
    if i > 0 and j > 0 and s1[i - 1] == s2[j - 1]:
      # coincidencia
      diff.append((' ', s1[i - 1]))
      i -= 1
      j -= 1
    else:
      # preferir eliminación sobre inserción (estilo Myers)
      if j > 0 and (i == 0 or L[i][j - 1] >= L[i - 1][j]):
        diff.append(('+', s2[j - 1]))
        j -= 1
      elif i > 0 and (j == 0 or L[i][j - 1] < L[i - 1][j]):
        diff.append(('-', s1[i - 1]))
        i -= 1

  diff.reverse()
  return diff


def git_diff_using_lcs_dynamic_lbl(s1, s2):
  # dividir en lineas en lugar de caracteres
  ls1 = s1.splitlines()
  ls2 = s2.splitlines()

  # calcular LCS para las lineas
  L, _, _ = lcs_dp(ls1, ls2)
  m, n = len(ls1), len(ls2)

  # reconstrucción diff
  i, j = m, n
  diff = []

  while i > 0 or j > 0:
    if i > 0 and j > 0 and ls1[i - 1] == ls2[j - 1]:
      # Coincidencia
      diff.append((' ', ls1[i - 1]))
      i -= 1
      j -= 1
    else:
      # Preferir eliminación sobre inserción (estilo Myers)
      if j > 0 and (i == 0 or L[i][j - 1] >= L[i - 1][j]):
        diff.append(('+', ls2[j - 1]))
        j -= 1
      elif i > 0 and (j == 0 or L[i][j - 1] < L[i - 1][j]):
        diff.append(('-', ls1[i - 1]))
        i -= 1

  diff.reverse()
  return diff


def format_diff(diff): return [f'{op}|{line}' for op, line in diff]


code_1 = """
x = 'Hello World'
print(x)
"""
code_2 = """
print('Hello World')
"""

if __name__ == "__main__":
  solution = git_diff_using_lcs_dynamic_lbl(code_1, code_2)
  # solution = git_diff_using_lcs_dynamic_cbc(code_1, code_2)
  format_solution = format_diff(solution)

  for diff in format_solution:
    print(diff)
