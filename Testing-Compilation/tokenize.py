def tokenize(text: str):
  tokens = []
  for item in text.split():
    tokens.append(item)
  return tokens

tokens = tokenize('5 + 3*2')
print(tokens)