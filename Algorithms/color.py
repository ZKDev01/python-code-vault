from typing import Any


class Graph:
  
  def __init__(self, adj_matrix: dict[ int, list[ int ] ] ) -> None:
    # comprobaciones
    self.adj_matrix = adj_matrix

  def get_subset_n_i ( self, i ) -> list[ int ]:
    subset_n_i = [ i ]


def color_main ( graph ) -> None:
  # 1. obtener lista en 0 para correspondencia: nodo-color
  # 2. obtener los subsets n_i 
  # 3. algoritmo desarrollado 
  ## 1. para la posicion i de la lista de correspondencia se comprueba el subset n_i y se tiene lo siguiente
  ## 2. +1 a la posicion i si value_i = value_j con j perteneciente a subset n_i 
  ## 3. se mantiene el valor i si value i != value_j con j perteneciente a subset n_i
  
  pass


def color_aux ( l: list[ int ], subsets: dict [ int, list[ int ] ] ):
  pass




def main ( ) -> None:
  
  pass

if __name__ == '__main__':
  
  main ( )

