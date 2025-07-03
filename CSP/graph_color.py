from meta_csp import *


def test_1():
  # tomar variables
  N = 5
  variables:List[Variable] = [ Variable(set(i for i in range(N))) for _ in range(N) ]
  
  func = lambda x,y: x.value != y.value
  c1 = Constract( 
    variables[0],variables[3], # (x_0,x_3) in E(G)
    func=func
  )
  c2 = Constract(
    variables[0],variables[4], # (x_0,x_4) in E(G)
    func=func
  )
  c3 = Constract(
    variables[1],variables[4], # (x_1,x_4) in E(G)
    func=func
  )
  c4 = Constract(
    variables[1],variables[2], # (x_1,x_2) in E(G)
    func=func
  )
  c5 = Constract(
    variables[2],variables[3], # (x_2,x_3) in E(G)
    func=func
  )
  c6 = Constract(
    variables[2],variables[4], # (x_2,x_4) in E(G)
    func=func
  )
  constracts = [ c1,c2,c3,c4,c5,c6 ]
  
  csp = MetaCSP(variables=variables,constracts=constracts)
  is_finded,solution = csp.chronological_backtracking()
  if is_finded:
    print(solution)



def main() -> None:
  test_1()

if __name__ == "__main__":
  main()
