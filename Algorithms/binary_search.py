
# Binary search is a faster searching algorithm for sorted arrays by repeatedly dividing the search interval in half

def binary_search( elements: list[int], target: int ) -> int:
  low, high = 0, len(elements) - 1
  while low <= high:
    mid = (low + high) // 2
    if elements[mid] == target:
      return mid
    elif elements[mid] < target:
      low = mid + 1
    else: 
      high = mid - 1
  return -1



def main() -> None:
  array = [ i for i in range(-10,10) ]
  target = 9

  array.sort()

  result = binary_search( array, target )
  print(f"""
  ARRAY: {array}
  TARGET: {target}
  ===========================================
  RESULT: {result}
  """)

if __name__ == '__main__':
  main()