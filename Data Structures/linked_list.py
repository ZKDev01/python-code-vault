
class Node:
  def __init__(self, value: int, next: 'Node' = None) -> None:
    self.value = value
    self.next = next

  def __str__(self) -> str:
    return f"""
    ==============================
    Value: {self.value}
    
    Next:
    ==============================
    {self.next}
    ==============================
    """

def main() -> None:
  node1 = Node( 1 )
  node2 = Node( 2, node1 )
  node3 = Node( 3, node2 )

  print(node3)

if __name__ == '__main__':
  main()