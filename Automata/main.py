from automata import FiniteAutomaton,DFA,NFA





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
  
  print(f"""
DFA que acepta cadenas terminadas en 'a'
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
  
  print(f"""
NFA que acepta cadenas que contiene '01'
  '001' es aceptada? <{nfa.accept('001')}>
  '010' es aceptada? <{nfa.accept('010')}>
  '111' es aceptada? <{nfa.accept('111')}>
  """)

  union_automaton = dfa.union(nfa)
  print(union_automaton)
  
  print(f"""
Unión de los autómatas
  'abba' es aceptada? <{union_automaton.accept('abba')}>
  '001' es aceptada? <{union_automaton.accept('001')}>
  '111abba' es aceptada? <{union_automaton.accept('111abba')}>
  """)

  converted_dfa = union_automaton.to_dfa()
  print(converted_dfa)

if __name__ == "__main__":
  main()
