
# merge-sort es un algortimo recursivo basico

def merge_sort (l: list[int]) -> list[int]:
  if len(l) == 1:
    return l
  
  ll = l[:len(l)//2]
  lr = l[len(l)//2:]

  ll = merge_sort(ll)
  lr = merge_sort(lr)

  return merge( ll,lr )

def merge (l1: list[int], l2: list[int]) -> list[int]:
  l = []

  while len(l1) > 0 and len(l2) > 0:
    if l1[0] < l2[0]:
      l.append(l1[0])
      l1 = l1[1:]
    else:
      l.append(l2[0])
      l2 = l2[1:]

  if len(l1) > 0:
    l = l + l1
  if len(l2) > 0:
    l = l + l2

  return l




def main() -> None:
  array1 = [ 20,19,16,15,10 ]
  result = merge_sort( array1 )
  print( f"Original:  {array1}" )
  print( f"Result:    {result}" )

if __name__ == '__main__':
  main()