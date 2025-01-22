

def square(num:int) -> int:
  return num**2

f = lambda x,y=2 : x**y

N = 10

# Use map function to process list items without using loops
x = [i for i in range(0,N+1)]
s = list( map(f,x) )

printer = f"""
x = {x}
s = {s}
"""
print (printer)

