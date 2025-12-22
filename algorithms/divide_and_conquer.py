import argparse
from typing import Iterable, Union

"""
Divide-and-Conquer: Paradigma que se basa en la resolución recursiva de un problema dividiéndolo en subproblemas disjuntos.
El proceso continúa hasta que estos subproblemas se puedan resolver de forma óptima.
Finalmente, las soluciones de los subproblemas se combinan para construir la solución del problema original.
"""


def _merge(
    left: Iterable[Union[int, float]],
    right: Iterable[Union[int, float]]
) -> Iterable[Union[int, float]]:
  result = []
  i = j = 0

  # compare elements and mix them in order
  while i < len(left) and j < len(right):
    if left[i] < right[j]:
      result.append(left[i])
      i += 1
    else:
      result.append(right[j])
      j += 1

  # add the remaining elements of the list that was not emptied
  result.extend(left[i:])
  result.extend(right[j:])
  return result


def mergesort(
    array: Iterable[Union[int, float]]
) -> Iterable[Union[int, float]]:
  # base case: list of size 0 or 1 is already "sorted"
  if len(array) <= 1:
    return array

  # divide
  mid = len(array) // 2
  l_half = array[:mid]  # subproblem 1: left half
  r_half = array[mid:]  # subproblem 2: right half

  # recursive calls
  l_sorted = mergesort(l_half)
  r_sorted = mergesort(r_half)

  # combine
  return _merge(l_sorted, r_sorted)


def mergesort_test() -> None:
  cases = [
      [38, 27, 43, 3, 9, 82, 10],
      [i for i in range(10, 0, -1)],
      [i for i in range(1000, 0, -1)]

  ]

  for index, case in enumerate(cases, 1):
    result = mergesort(case)
    response = sorted(case)
    print(f"{index}. Case {case} (N={len(case)}): {result == response}")
# endregion


def main() -> None:
  options = {"mergesort": mergesort_test}
  parser = argparse.ArgumentParser()
  parser.add_argument('function', choices=options.keys())

  args = parser.parse_args()
  options[args.function]()


if __name__ == "__main__":
  main()
