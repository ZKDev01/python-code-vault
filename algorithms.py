from typing import List


def binary_search (element:List[int], target:int) -> int:
  """Binary Search Algorithm 

  Binary search is a faster searching algorithm for sorted arrays by repeatedly dividing the search interval in half

  Args:
      element (List[int]): _description_
      target (int): _description_

  Returns:
      int: _description_
  """
  a = 0
  b = len(element)-1

  while a <= b:
    tmp = (a + b) // 2
    if element[tmp] == target:
      return tmp
    elif element[tmp] < target:
      a = tmp + 1
    else:
      b = tmp - 1
  
  return -1


def bubble_sort (items: List[int]) -> List[int]:
  """

  Args:
      items (List[int]): _description_

  Returns:
      List[int]: _description_
  """
  n = len(items)

  for _ in range ( 1, n ):
    for j in range ( 0, n-1 ):
      if items[j] > items[j+1]:
        tmp = items[j]
        items[j] = items[j+1]
        items[j+1] = tmp

  return items



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
  array = [ i**2 for i in range(100) ]
  target = 9

  result = binary_search (array, target)
  print(result)
  

if __name__ == "__main__":
  main()
  
  
  