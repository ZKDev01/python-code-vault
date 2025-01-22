from typing import List,Set




class Basic_Disjoint_Set :
  def __init__(self, n:int):
    self.sets = [ {i+1} for i in range(n) ]
    self.n = n 

  def add_set(self):
    self.sets += [{self.n+1}]
    self.n += 1

  def find_set(self, x:int):
    for s in self.sets:
      if x in s:
        return s
    return False

  #! fail 
  def union(self, x:int,y:int):
    x:set=self.find_set(x)
    y=self.find_set(y)
    x.update(y)
    del self.sets[y] 
  
  def show(self):
    for i,s in enumerate(self.sets):
      print( f"{i+1}. {s}" )


def main() -> None:
  ds = Basic_Disjoint_Set(10)
  ds.add_set()
  ds.show()
  ds.union(1,2)
  ds.show()


if __name__ == '__main__' : 
  main()
