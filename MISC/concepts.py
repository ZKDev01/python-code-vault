import glob


def test_1() -> None:
  def fn1(*x):
    print (type(x))
    print (x)

  def fn2(**x):
    print (type(x))
    print (x)

  fn1(1,2,3,4)
  fn2(a=1,b=2,c=3,d=4)

def test_2() -> None:
  x = 0

  def outer():
    x = 1
    
    def inner():
      nonlocal x
      print(f"inner: {x}")
    
    inner()
    print(f"outer: {x}")

  outer()
  print(f"global: {x}") 

  """
  output:
    inner: 1 
    outer: 1
    global: 0
  """

def test_3() -> None:
    
  c = 1 # global variable
  def show ():
    print (c)
  show() # output: 1

  c = 1
  def add ():
    c = c + 2
    print (c)
  add() # <ERROR> UnboundLocalError: local variable 'c' referenced before assignment

  c = 1
  def add():
    global c # use of global keyword
    c = c + 1
    print (c)
  add() # output: 2

def test_4() -> None:
  x = 1
  y = 1
  print (id(x))   # 140726857451960
  print (id(y))   # 140726857451960
  print (x is y)  # True

def test_5() -> None:
  dict_elements = {'counter':0}

  def foo1():
    dict_elements['counter'] += 1
    
  def foo2():
    dict_elements['counter'] += 1  
    foo1()

  foo2()
  print(dict_elements['counter'])   # 2 

  dict_elements = {'counter':0}

  def foo3(x):
    x['counter'] += 1

  foo3(dict_elements)
  print(dict_elements['counter'])   # 1

def test_5() -> None:
  def add_one(x):
    x[0] += 1

  try:
    s = set(1)
    add_one(s)
    print (s)
  except Exception as e:
    print (e)
  # 'int' object is not iterable

  try:
    s = list(1)
    add_one(s)
  except Exception as e:
    print (e)
  # 'int' object is not iterable

  try:
    s = [1]
    add_one(s)
    print (s)
  except Exception as e:
    print (e)
  # [2]

def test_6() -> None:
  y = 1
  x = y
  print (x is y)  # True
  y = 2
  print (x)       # 1
  print (x is y)  # False
  y+= 1
  print (x)       # 1
  print (x is y)  # False

  y = 1
  x = y
  print (x is y)  # True
  y+= 1
  print (x)       # 1
  print (x is y)  # False
  y = 2
  print (x)       # 1
  print (x is y)  # False

def test_7() -> None:
  l = [1,2,3,4]
  print (id(l))  # 1905648326912
  l += [5]
  print (id(l))  # 1905648326912
  l.append(6)
  print (id(l))  # 1905648326912
  l = [4,3,2,1]
  print (id(l))  # 1905648324992

def test_8() -> None:
  x = 4
  print (id(x)) # 140726857452056
  x+= 1
  print (id(x)) # 140726857452088

  s = "python"
  print (id(s)) # 2499532995680
  s+= " language programming"
  print (id(s)) # 2499533396832

  try:
    s[0] = "P"
  except Exception as e:
    print(e)
  # 'str' object does not support item assignment



if __name__ == "__main__":
  test_1()
  #test_2()
  #test_3()
  #test_4()
  #test_5()
  #test_6()
  #test_7()
  #test_8()
