from typing import List


def _swap(array: List[int], index_a: int, index_b: int) -> None:
  tmp = array[index_a]
  array[index_a] = array[index_b]
  array[index_b] = tmp


def largest_permutation(array: List[int], possible_swap: int) -> None:
  "Implementación Greedy"
  N = len(array)

  candidates = []
  # 1. Iterar sobre la lista para obtener una lista de candidatos (elemen)
  for index in range(N):
    if array[index] - 1 == index:
      candidates.append(index)

  N_candidates = len(candidates)
  for index in range(N_candidates - 1):
    if possible_swap > 0:
      _swap(array, candidates[index], candidates[index + 1])
      possible_swap -= 1


def main() -> None:
  array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
  print(array)
  largest_permutation(
      array=array,
      possible_swap=len(array) // 2
  )
  print(array)


if __name__ == "__main__":
  main()
