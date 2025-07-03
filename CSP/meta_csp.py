from typing import Any, Dict, List, Set, Tuple

class Variable:
  def __init__(self,domain:Set,v_default=None):
    self.value = v_default
    self.domain = domain
  
  def get_value(self) -> Any:
    "Valor asignado de la variable"
    return self.value
  
  def get_domain(self) -> Set:
    "Dominio de la variable"
    return self.domain
  
  def accept(self, v) -> None:
    "Asigna/acepta un valor del dominio a la variable"
    if v in self.domain:
      self.value = v
  
  def reject(self) -> None:
    "Rechaza el valor actual de la variable y lo asigna a null"
    self.value = None
  
  def __repr__(self) -> str:
    return f"Variable = {self.value}\n => <D_x = {self.domain}>\n"

class Constract:
  def __init__(self,*vars:List[Variable],func) -> None:
    self.vars = vars
    self.func = func
  
  def check_constract(self) -> bool:
    return self.func(*self.vars)

class Solution:
  def __init__(self, variables:List[Variable], constracts:List[Constract]) -> None:
    self.variables:List[Variable] = variables
    self.constracts:List[Constract] = constracts
  
  def is_terminal(self) -> bool:
    "Todos las variables tienen un valor del dominio (no importa que no cumpla las restricciones)"
    for variable in self.variables:
      if variable.value == None: return False
    return True
  
  def is_valid(self) -> bool:
    "Todas las restricciones se cumplen sin importar la asignacion de las variables"
    checkers = [ constract.check_constract() for constract in self.constracts ]
    return all(checkers)
  
  def is_solution(self) -> bool:
    return self.is_terminal() and self.is_valid()
  
  def reset(self) -> None:
    for variable in self.variables:
      variable.value == None
  
  def __repr__(self) -> str:
    output = ""
    for i,variable in enumerate(self.variables):
      output += f"Var_{i} = {variable.value}\n"
    return output

class MetaCSP:
  def __init__(self, variables:List[Variable], constracts:List[Constract] ) -> None:
    self.variables:List[Variable] = variables
    self.constracts:List[Constract] = constracts
    self.solution = Solution(variables,constracts)

  def chronological_backtracking(self):
    self.solution.reset()
    is_finded = self._aux_cb()
    if is_finded:
      return is_finded,self.solution
    return is_finded,None
  
  def _aux_cb(self):
    if self.solution.is_solution():
      return True
    if self.solution.is_terminal():
      return False
    index = self._find_var_without_assign()
    variable:Variable = self.variables[index]
    for value in variable.domain:
      variable.accept(value)
      is_solution = self._aux_cb()
      if is_solution:
        return is_solution
      variable.reject()
    return False 
  
  def _find_var_without_assign(self) -> int:
    for index,variable in enumerate(self.variables):
      if variable.value == None: return index
    return -1

  def _check_partial_solution(self) -> bool:
    # TODO
    pass

