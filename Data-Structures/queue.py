from collections import deque

def make_queue( items: list[int] ) -> None:
  queue = deque(items)

  # dequeueing elements
  item = queue.popleft()
  print(item)

def main() -> None:
  make_queue ( items= [ i for i in range(0,10) ] )

if __name__ == '__main__':
  main()