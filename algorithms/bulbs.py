# Problema "Bulbs" (Bombillas)
# Descripción: Al activar la bombilla i se invierten todas las bombillas a la derecha
# Entrada: Array 0/1 (0: off, 1: on)
# Objetivo: Minimizar Cambios para Encender Todas las Bombillas

from typing import List


def solve_greedy(a: List[bool]):
  paridad = 0
  for bulb in a:
    if (not (paridad % 2) and not bulb) or ((paridad % 2) and bulb):
      paridad += 1
  return paridad


def main(*args, **kwargs) -> None:
  bulbs = [True, False, False, True]
  print(solve_greedy(bulbs))


if __name__ == "__main__":
  main()
