
# Graphs consist of vertices and edges that connect them

class Vertex:
  def __init__(self, tag: str) -> None:
    self.tag = tag
  def __str__(self) -> str:
    return f"Vertex Value: {self.tag}"

class Graph: 
  def __init__(self, vertex: list[Vertex], edges: dict[ Vertex, dict[Vertex, int] ]) -> None:
    self.vertex = vertex
    self.edges = edges

  def __str__(self) -> str:
    t_vertex = '======= VERTEX =======\n\n'
    t_edges = '======= EDGES =======\n\n'
    for v in self.vertex: 
      
      t_vertex = t_vertex + v.__str__() + "\n"
      
    text = f"""
      {t_vertex}
      {t_edges}
    """
    return text



def main() -> None:
  v1 = Vertex("A")
  v2 = Vertex("B")
  v3 = Vertex("C")
  v4 = Vertex("D")
  v5 = Vertex("E")
  v6 = Vertex("F")
  v7 = Vertex("G")
  
  edges = { }
  edges[ v1 ] = {
    v2: 2,
    v3: 4,
    v4: 8,
    v5: 16,
  }  
  edges[ v2 ] = {
    v3: 3,
    v4: 6,
    v6: 9,
  }
  edges[ v4 ] = {
    v5: 5,
    v6: 10,
    v7: 15,
  }
  edges[ v6 ] = {
    v7: 10
  }

  graph = Graph( vertex=[v1,v2,v3,v4,v5,v6,v7], edges=edges )
  print(graph)


if __name__ == '__main__':
  main()

