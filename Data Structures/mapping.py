from collections import Counter, defaultdict

def counter_string ( line: str ) -> Counter:
  obj = Counter(line)
  print(obj)
  return obj

def main () -> None:
  tmp = 'aabbc'
  counter_string(tmp)

if __name__ == '__main__':
  main()

