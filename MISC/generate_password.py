import random

lower = "qwertyuiopasdfghjklzxcvbnm"
upper = "QWERTYUIOPASDFGHJKLZXCVBNM"
numbers = "0123456789"
symbols = "[]{}()*;/,._-"

characters = lower + upper + numbers + symbols

def main() -> None:
  length = 16
  password = "".join(random.sample(characters, length))
  print(password)

if __name__ == "__main__":
  main()