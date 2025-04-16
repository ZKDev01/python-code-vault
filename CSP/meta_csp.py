
from typing import Any, Dict, List, Tuple

from numpy import var

# HERE is DOMAIN
class Variable:
  def get_assign_value(self) -> Any:
    try: 
      return self.value
    except:
      raise(...)
  
  def get_domain_variable(self) -> List:
    return []
  
  def get_possible_values(self) -> List:
    return []
  
  def accept(self) -> None:
    ...
  
  def reject(self) -> None:
    ...

class Constracts:
  pass

class Solution:
  def __init__(self):
    ...
  
  def is_terminal(self):
    ...
  
  def is_all_variables(self):
    ...
  
  def is_valid(self):
    ...
  
  def reset(self):
    ...

class MetaCSP:
  def __init__(self,
    variables:List[Variable],
    constracts:List[Constracts]
    ) -> None:
    self.variables = variables
    self.constracts = constracts
    self.solution = None

  def chronological_backtracking(self):
    self.solution.reset()
    is_finded = self._aux_cb()
    if is_finded:
      return is_finded,self.solution
    return is_finded,None
  
  def _aux_cb(self):
    if self.solution.is_terminal():
      return True
    index = self._find_var_without_assign()
    variable:Variable = self.variables[index]
    for value in variable.get_possible_values():
      variable.accept(value)
      if self._check_partial_solution():
        return self._aux_cb()
      variable.reject(value)
    return False
  
  def _find_var_without_assign(self) -> int:
    ...

  def _check_partial_solution(self) -> bool:
    ...

