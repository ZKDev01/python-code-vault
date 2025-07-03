from meta_csp import *


def test_1():
  N = 8
  variables:List[Variable] = [ Variable(set(i for i in range(N))) for _ in range(N) ]

  # R_i != R_j, para todo i != j, con 1 <= i,j <= N
  func_1 = lambda x,y: x.value != y.value 
  # |R_i - R_j| != |i - j|, para todo i != j, con 1 <= i,j <= N
  func_2 = lambda x,y,_i,_j: abs(x.value - y.value) != abs(_i-_j)
  
  constracts = []
  for i in range(N):
    for j in range(N):
      if i != j:
        constracts.append( Constract( variables[i],variables[j], func=func_1) ) # forall i,j . i != j
        constracts.append( Constract( variables[i],variables[j],i,j, func=func_2) ) # forall i,j . i != j

  csp = MetaCSP(variables=variables,constracts=constracts)
  is_finded,solution = csp.chronological_backtracking()
  if is_finded:
    print(solution)


def main() -> None:
  test_1()

if __name__ == "__main__":
  main()
