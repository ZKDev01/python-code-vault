from typing import Set, Dict
from collections import deque
from abc import ABC, abstractmethod

EPSILON = 'ε'


class FiniteAutomaton(ABC):
  "Clase abstracta base para autómatas finitos. Interfaz común para DFA y NFA"

  def __init__(self,
               states: Set[str],
               alphabet: Set[str],
               initial_state: str,
               final_states: Set[str]
               ) -> None:
    """Inicializa los componentes básicos del autómata

    Args:
      states (Set[str]): conjunto de estados del autómata
      alphabet (Set[str]): alfabeto del lenguaje
      initial_state (str): estado inicial
      final_states (Set[str]): conjunto de estados finales
    """
    self.states: Set[str] = states
    self.alphabet: Set[str] = alphabet
    self.initial_state: str = initial_state
    self.final_states: Set[str] = final_states

  @abstractmethod
  def accept(self, input_string: str) -> bool:
    """Determina si una cadena es aceptada por el autómata

    Args:
      input_string (str): cadena a verificar

    Returns:
      bool: True si la cadena es aceptada, False en caso contrario
    """
    pass

  @abstractmethod
  def concatenate(self, other: 'FiniteAutomaton') -> 'NFA':
    """Concatena dos autómatas.

    Args:
      other (FiniteAutomaton): otro autómata a concatenar

    Returns:
      NFA: nuevo NFA que reconoce la concatenación de dos autómatas
    """
    pass

  @abstractmethod
  def union(self, other: 'FiniteAutomaton') -> 'NFA':
    """Crea la unión de dos autómatas

    Args:
        other (FiniteAutomaton): otro autómata para la unión

    Returns:
        NFA: nuevo NFA que reconoce la unión de dos autómatas
    """
    pass

  @abstractmethod
  def kleene_closure(self) -> 'NFA':
    """Aplica la clausura de Kleene (estrella) al autómata.

    Returns:
      NFA: nuevo NFA que reconoce la clausura de Kleene del lenguaje
    """
    pass


class DFA(FiniteAutomaton):
  "Implementación de un Autómata Finito Determinista (DFA)"

  def __init__(self,
               states: Set[str],
               alphabet: Set[str],
               transitions: Dict[str, Dict[str, str]],
               initial_state: str,
               final_states: Set[str]
               ) -> None:
    super().__init__(states, alphabet, initial_state, final_states)
    self.transitions: Dict[str, Dict[str, str]] = transitions

  def accept(self, input_string: str) -> bool:
    current_state = self.initial_state

    for symbol in input_string:
      if symbol not in self.alphabet:
        return False

      if current_state not in self.transitions or symbol not in self.transitions[current_state]:
        return False

      current_state = self.transitions[current_state][symbol]

    return current_state in self.final_states

  def concatenate(self, other: FiniteAutomaton) -> 'NFA':
    # Convertir ambos autómatas a NFA para facilitar la concatenación
    self_nfa = self.to_nfa()
    if isinstance(other, DFA):
      other_nfa = other.to_nfa()
    else:
      other_nfa = other

    return self_nfa.concatenate(other_nfa)

  def union(self, other: FiniteAutomaton) -> 'NFA':
    # Convertir ambos autómatas a NFA para facilitar la unión
    self_nfa = self.to_nfa()
    if isinstance(other, DFA):
      other_nfa = other.to_nfa()
    else:
      other_nfa = other

    return self_nfa.union(other_nfa)

  def kleene_closure(self) -> 'NFA':
    return self.to_nfa().kleene_closure()

  def to_nfa(self) -> 'NFA':
    """Convierte el DFA a un NFA equivalente

    Returns:
        NFA: NFA equivalente a un NFA equivalente
    """
    # Convertir transiciones de DFA a formato NFA
    nfa_transitions = {}
    for state, trans in self.transitions.items():
      nfa_transitions[state] = {}
      for symbol, dest_state in trans.items():
        nfa_transitions[state][symbol] = {dest_state}

    return NFA(
        states=self.states.copy(),
        alphabet=self.alphabet.copy(),
        transitions=nfa_transitions,
        initial_state=self.initial_state,
        final_states=self.final_states.copy()
    )

  def __str__(self) -> str:
    return f"DFA (Autómata Finito Determinista):\nEstados: {self.states}\nAlfabeto: {self.alphabet}\nEstado Inicial: {self.initial_state}\nEstados Finales: {self.final_states}\nTransiciones: {self.transitions}"

  def __repr__(self):
    return self.__str__()


class NFA(FiniteAutomaton):
  "Implementación de un Autómata Finito no Determinista (NFA)"

  def __init__(self,
               states: Set[str],
               alphabet: Set[str],
               transitions: Dict[str, Dict[str, Set[str]]],
               initial_state: str,
               final_states: Set[str]
               ) -> None:
    super().__init__(states, alphabet, initial_state, final_states)
    self.transitions: Dict[str, Dict[str, Set[str]]] = transitions

  def accept(self, input_string: str) -> bool:
    current_states = {self.initial_state}

    # Aplicar epsilon-clausura al estado inicial
    current_states = self._epsilon_closure(current_states)

    for symbol in input_string:
      if symbol not in self.alphabet:
        return False

      next_states = set()
      for state in current_states:
        if state in self.transitions and symbol in self.transitions[state]:
          next_states.update(self.transitions[state][symbol])

      current_states = self._epsilon_closure(next_states)

      if not current_states:
        return False

    return bool(current_states.intersection(self.final_states))

  def _epsilon_closure(self, states: Set[str]) -> Set[str]:
    """Calcula la epsilon-clausura de un conjunto de estados

    Args:
      states (Set[str]): conjunto de estados inicial

    Returns:
      Set[str]: conjunto de estados alcanzables por epsilon-transiciones
    """
    closure = set(states)
    stack = list(states)

    while stack:
      state = stack.pop()
      if state in self.transitions and EPSILON in self.transitions[state]:
        for eps_state in self.transitions[state][EPSILON]:
          if eps_state not in closure:
            closure.add(eps_state)
            stack.append(eps_state)

    return closure

  def concatenate(self, other: FiniteAutomaton) -> 'NFA':
    # Convertir el otro autómata a NFA si es necesario
    if isinstance(other, DFA):
      other = other.to_nfa()

    # Renombrar estados para evitar conflictos
    self_states = {f"L_{state}" for state in self.states}
    other_states = {f"R_{state}" for state in other.states}

    # Construir nuevos conjuntos
    new_states = self_states.union(other_states)
    new_alphabet = self.alphabet.union(other.alphabet)
    new_initial_state = f"L_{self.initial_state}"
    new_final_states = {f"R_{state}" for state in other.final_states}

    # Construir transiciones
    new_transitions = {}

    # Copiar transiciones del primer autómata
    for state, trans in self.transitions.items():
      new_state = f"L_{state}"
      new_transitions[new_state] = {}
      for symbol, dest_set in trans.items():
        new_transitions[new_state][symbol] = {f"L_{dest}" for dest in dest_set}

    # Copiar transiciones del segundo autómata
    for state, trans in other.transitions.items():
      new_state = f"R_{state}"
      new_transitions[new_state] = {}
      for symbol, dest_set in trans.items():
        new_transitions[new_state][symbol] = {f"R_{dest}" for dest in dest_set}

    # Agregar epsilon-transiciones desde estados finales del primer autómata
    # al estado inicial del segundo autómata
    for final_state in self.final_states:
      left_final = f"L_{final_state}"
      if left_final not in new_transitions:
        new_transitions[left_final] = {}
      if EPSILON not in new_transitions[left_final]:
        new_transitions[left_final][EPSILON] = set()

      new_transitions[left_final][EPSILON].add(f"R_{other.initial_state}")

    return NFA(
        states=new_states,
        alphabet=new_alphabet,
        transitions=new_transitions,
        initial_state=new_initial_state,
        final_states=new_final_states
    )

  def union(self, other: FiniteAutomaton) -> 'NFA':
    # Convertir el otro autómata a NFA si es necesario
    if isinstance(other, DFA):
      other = other.to_nfa()

    # Renombrar estados para evitar conflictos
    self_states = {f"L_{state}" for state in self.states}
    other_states = {f"R_{state}" for state in other.states}

    # Crear nuevo estado inicial
    new_initial_state = "q_start"
    new_states = self_states.union(other_states).union({new_initial_state})
    new_alphabet = self.alphabet.union(other.alphabet)
    new_final_states = {f"L_{state}" for state in self.final_states}.union(
        {f"R_{state}" for state in other.final_states}
    )

    # Construir transiciones
    new_transitions = {
        new_initial_state: {
            EPSILON: {f"L_{self.initial_state}", f"R_{other.initial_state}"}
        }
    }

    # Copiar transiciones del primer autómata
    for state, trans in self.transitions.items():
      new_state = f"L_{state}"
      new_transitions[new_state] = {}
      for symbol, dest_set in trans.items():
        new_transitions[new_state][symbol] = {f"L_{dest}" for dest in dest_set}

    # Copiar transiciones del segundo autómata
    for state, trans in other.transitions.items():
      new_state = f"R_{state}"
      new_transitions[new_state] = {}
      for symbol, dest_set in trans.items():
        new_transitions[new_state][symbol] = {f"R_{dest}" for dest in dest_set}

    return NFA(
        states=new_states,
        alphabet=new_alphabet,
        transitions=new_transitions,
        initial_state=new_initial_state,
        final_states=new_final_states
    )

  def kleene_closure(self) -> 'NFA':
    # Renombrar estados del autómata original
    original_states = {f"orig_{state}" for state in self.states}

    # Crear nuevos estados
    new_initial_state = "q_start"
    new_final_state = "q_final"
    new_states = original_states.union({new_initial_state, new_final_state})
    new_alphabet = self.alphabet.copy()
    new_final_states = {new_final_state}

    # Construir transiciones
    new_transitions = {}

    # Epsilon-transición desde el nuevo estado inicial
    new_transitions[new_initial_state] = {
        EPSILON: {f"orig_{self.initial_state}", new_final_state}
    }

    # Copiar transiciones del autómata original
    for state, trans in self.transitions.items():
      new_state = f"orig_{state}"
      new_transitions[new_state] = {}
      for symbol, dest_set in trans.items():
        new_transitions[new_state][symbol] = {f"orig_{dest}" for dest in dest_set}

    # Epsilon-transiciones desde estados finales originales
    for final_state in self.final_states:
      orig_final = f"orig_{final_state}"
      if orig_final not in new_transitions:
        new_transitions[orig_final] = {}
      if EPSILON not in new_transitions[orig_final]:
        new_transitions[orig_final][EPSILON] = set()

      new_transitions[orig_final][EPSILON].update({
          f"orig_{self.initial_state}",  # Para repetir
          new_final_state  # Para terminar
      })

    return NFA(
        states=new_states,
        alphabet=new_alphabet,
        transitions=new_transitions,
        initial_state=new_initial_state,
        final_states=new_final_states
    )

  def to_dfa(self) -> DFA:
    """Convierte el NFA a un DFA equivalente usando construcción de subconjuntos

    Returns:
      DFA: equivalente al NFA
    """
    # Estados del DFA serán conjuntos de estados del NFA
    dfa_states = set()
    dfa_transitions = {}
    dfa_final_states = set()

    # Estado inicial del DFA
    initial_closure = self._epsilon_closure({self.initial_state})
    dfa_initial_state = frozenset(initial_closure)
    dfa_states.add(dfa_initial_state)

    # Queue para procesamiento BFS
    queue = deque([dfa_initial_state])
    processed = set()

    while queue:
      current_dfa_state = queue.popleft()
      if current_dfa_state in processed:
        continue
      processed.add(current_dfa_state)

      # Verificar si es estado final
      if current_dfa_state.intersection(self.final_states):
        dfa_final_states.add(current_dfa_state)

      # Procesar transiciones para cada símbolo del alfabeto
      dfa_transitions[current_dfa_state] = {}
      for symbol in self.alphabet:
        if symbol == 'ε':
          continue

        next_states = set()
        for nfa_state in current_dfa_state:
          if nfa_state in self.transitions and symbol in self.transitions[nfa_state]:
            next_states.update(self.transitions[nfa_state][symbol])

        if next_states:
          next_closure = self._epsilon_closure(next_states)
          next_dfa_state = frozenset(next_closure)
          dfa_transitions[current_dfa_state][symbol] = next_dfa_state

          if next_dfa_state not in dfa_states:
            dfa_states.add(next_dfa_state)
            queue.append(next_dfa_state)

    # Convertir frozensets a strings para compatibilidad
    state_mapping = {state: f"q{i}" for i, state in enumerate(dfa_states)}

    new_states = set(state_mapping.values())
    new_transitions = {}
    new_initial_state = state_mapping[dfa_initial_state]
    new_final_states = {state_mapping[state] for state in dfa_final_states}

    for old_state, transitions in dfa_transitions.items():
      new_state = state_mapping[old_state]
      new_transitions[new_state] = {}
      for symbol, dest_state in transitions.items():
        new_transitions[new_state][symbol] = state_mapping[dest_state]

    return DFA(
        states=new_states,
        alphabet=self.alphabet - {'ε'},  # Remover epsilon del alfabeto
        transitions=new_transitions,
        initial_state=new_initial_state,
        final_states=new_final_states
    )

  def __str__(self) -> str:
    return f"NFA (Autómata Finito no Determinista):\nEstados: {self.states}\nAlfabeto: {self.alphabet}\nEstado Inicial: {self.initial_state}\nEstados Finales: {self.final_states}\nTransiciones: {self.transitions}"

  def __repr__(self):
    return self.__str__()


def main() -> None:
  # Crear un DFA simple que acepta cadenas que terminan en 'a'
  dfa = DFA(
      states={'q0', 'q1'},
      alphabet={'a', 'b'},
      transitions={
          'q0': {'a': 'q1', 'b': 'q0'},
          'q1': {'a': 'q1', 'b': 'q0'}
      },
      initial_state='q0',
      final_states={'q1'}
  )

  print(dfa)

  print(f"""DFA que acepta cadenas terminadas en 'a'
  'abba' es aceptada? <{dfa.accept('abba')}>
  'abbb' es aceptada? <{dfa.accept('abbb')}>
  'ba' es aceptada? <{dfa.accept('ba')}>
  """)

  # Crear un NFA simple que acepta cadenas que contienen '01'
  nfa = NFA(
      states={'p0', 'p1', 'p2'},
      alphabet={'0', '1'},
      transitions={
          'p0': {'0': {'p0', 'p1'}, '1': {'p0'}},
          'p1': {'1': {'p2'}},
          'p2': {'0': {'p2'}, '1': {'p2'}}
      },
      initial_state='p0',
      final_states={'p2'}
  )

  print(nfa)

  print(f"""NFA que acepta cadenas que contiene '01'
  '001' es aceptada? <{nfa.accept('001')}>
  '010' es aceptada? <{nfa.accept('010')}>
  '111' es aceptada? <{nfa.accept('111')}>
  """)

  union_automaton = dfa.union(nfa)
  print(union_automaton)

  print(f"""Unión de los autómatas
  'abba' es aceptada? <{union_automaton.accept('abba')}>
  '001' es aceptada? <{union_automaton.accept('001')}>
  '111abba' es aceptada? <{union_automaton.accept('111abba')}>
  """)

  converted_dfa = union_automaton.to_dfa()
  print(converted_dfa)


if __name__ == "__main__":
  main()
