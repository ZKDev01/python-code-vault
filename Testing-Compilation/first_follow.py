
grammar = [
  ('E', 'T E'),
  ('E', 'T'),
  ('T', 'F T'),
  ('T', 'F'),
  ('F', '( E )'),
  ('F', '0'),
]

def FIRST(grammar: str):
  first = {}
  for no_terminal in grammar:
    first[no_terminal] = set()
    for production in grammar:
      if production[0] == no_terminal:
        for symbol in production[1].split():
          if symbol.isupper():
            first[no_terminal].add(symbol)
          elif symbol.islower() or symbol.isdigit():
            first[no_terminal].add(symbol)
            break
  return first
