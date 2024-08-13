
# O(n^2)

def bubble_sort (items: list[int]) -> list[int]:
  n = len( items )

  for _ in range ( 1, n ):
    for j in range ( 0, n-1 ):
      if items[j] > items[j+1]:
        tmp = items[j]
        items[j] = items[j+1]
        items[j+1] = tmp

  return items

def main() -> None:
  array1 = [ 20,19,18,17,16,15,14,13,12,11 ]
  print( f"Original:  {array1}" )
  bubble_sort( array1 )
  print( f"Results:   {array1}" )

if __name__ == '__main__':
  main()
