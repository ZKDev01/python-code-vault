import numpy as np

def create_and_print_arrays():
  """
  Create and display NumPy arrays with different dimensions and values. 
  Include examples of arrays with specific values, empty arrays, zeros, ones, and filled with a specific value. 
  Also show how to create an array with random values.
  """

  a1 = np.array([1,2,3])
  print(a1)

  a2 = np.array([ [1,2,3],[4,5,6] ])
  print(a2)

  a3 = np.array([ [[1,2],[3,4]],[[5,6],[7,8]] ])
  print(a3)
  
  dimension = 2  

  empty = np.empty(dimension)
  print(empty)

  zeros = np.zeros(dimension)
  print(zeros)

  ones = np.ones(dimension)
  print(ones)

  full = np.full(dimension, 2)
  print(full)

  identity = np.identity(dimension)
  print(identity)

  random = np.random.random(size=dimension)
  print(random)

def attr_array(array: np.ndarray):
  """
  Method that shows the main attributes that an array has
  """
  print("Number of dimensions of the array:", array.ndim)
  print("Tuples with the dimensions of the array:", array.shape)
  print("Number of elements in the array:", array.size)
  print("Data type of the elements in the array:", array.dtype)

if __name__ == "__main__":
  create_and_print_arrays()
  attr_array(np.array([[1,2,3],[2,3,5]]))

  testing = np.array([[1,2],[3,4]])
  print(testing[1][1])
  testing[1][1]=30
  print(testing[1][1])

  """
  A very useful feature of arrays is that 
  it is very easy to obtain another array with the elements 
  that meet a condition.
  """
  results = testing[(testing % 3 == 0)]
  print(results)