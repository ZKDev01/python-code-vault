# Problema: Disjoint Intervals
# Descripción: Dado un conjunto de intervalos, encontrar el tamaño máximo de un subconjunto de intervalos mutuamente disjuntos (sin solapamientos)

from typing import List, Tuple


def disjoint_intervals(intervals: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
  "Complejidad Temporal del Algoritmo: O(n log n)"
  asc_intervals = sorted(intervals, key=lambda i: i[1], reverse=False)
  pointer = 0
  max_intervals = [asc_intervals[pointer]]
  for index in range(1, len(asc_intervals)):
    tmp_interval = asc_intervals[index]
    current_interval = asc_intervals[pointer]
    if current_interval[1] < tmp_interval[0]:
      pointer = index
      max_intervals.append(tmp_interval)
  return max_intervals


def main() -> None:
  intervals = [(1, 2), (1, 3), (1, 4), (1, 5), (3, 5), (6, 10), (3, 5), (5, 6), (6, 8)]
  max_intervals = disjoint_intervals(intervals)
  print(max_intervals)


if __name__ == "__main__":
  main()
