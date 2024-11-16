from typing import Set, Dict

class Graph:
  def __init__(self, vertex: Set[int], edges: Dict[int, Set[int]] ) -> None:
    self.vertex = vertex
    self.edges = edges

  def __str__(self) -> str:
    tmp_vertex = [ str(i) for i in self.vertex ]
    return "Vertex -> {" + '-'.join(tmp_vertex) + "}" 

def main ( ) -> None:
  N = 10
  graph = Graph(
    vertex= { i for i in range ( N ) },
    edges= { i: set( ) for i in range ( N ) }
  )

  print ( graph )

if __name__ == '__main__':
  main ( )