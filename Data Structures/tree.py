
# Trees are hierarchical data structures with nodes connected by edges

class Node: 
  def __init__(self, value: int, children: list['Node'] = [], parent: 'Node' = None) -> None:
    self.value = value
    self.parent = parent
    self.children = children

  def set_children( self, children: list['Node'], clean: bool ) -> None:
    if clean:
      self.children = children
    else:
      [ self.children.append(child) for child in children ]

  def __str__(self) -> str:
    return f"VALUE: {self.value}"



def main() -> None:
  root = Node( value= 10 )
  child_1 = Node( value= 2, parent= root )
  child_2 = Node( value= 3, parent= root ) 
  child_3 = Node( value= 4, parent= root )
  root.set_children( children= [ child_1, child_2 ], clean= False )
  root.set_children( children= [ child_1, child_2, child_3 ], clean= True)

  for i in root.children:
    print(i)

if __name__ == '__main__':
  main()

