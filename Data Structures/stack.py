
# Stacks follow the Last In First Out (LIFO) principle


def make_stack(items: list[int]) -> None:
  stack = items
  print(stack)

  # Pop elements
  item = stack.pop()
  print(item)




def main() -> None:
  make_stack( items= [ i for i in range(0,10) ] )


if __name__ == '__main__':
  main()

