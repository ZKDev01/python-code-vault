from typing import List

def bubble_sort (items: List[int]) -> List[int]:
  n = len( items )

  for _ in range ( 1, n ):
    for j in range ( 0, n-1 ):
      if items[j] > items[j+1]:
        tmp = items[j]
        items[j] = items[j+1]
        items[j+1] = tmp

  return items

def main() -> None:

  array = [ 20,19,18,17,16,15,14,13,12,11 ]
  print( f"Original:  {array}" )
  bubble_sort( array )
  print( f"Results:   {array}" )

if __name__ == '__main__':
  main()
