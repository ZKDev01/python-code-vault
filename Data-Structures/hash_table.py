
# Hash tables store KEY-VALUE pairs and provide efficient lookup

def make_hash_table () -> None:
  hash_table = { }

  print( "Leave the input empty to not add more elements" )
  while True:
    key = input( "Give me a key: " )
    if not key:
      break
    value = input( f"Give me a value for key -> {key}: " )
    hash_table[ key ] = value

  text = f""" THE HASH TABLE is: 
  {hash_table}
  """
  print( text )



def main() -> None:
  make_hash_table()

if __name__ == "__main__":
  main()