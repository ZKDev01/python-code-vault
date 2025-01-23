import os 
import numpy as np 
import matplotlib.pyplot as plt

from faker import Faker
from typing import List,Set,Any




BOW_MUSIC = [
  'jazz',
  'rock',
  'pop',
  'classical',
  'hip-hop'
]



class DataGenerator:
  def __init__(self, bow:List[str], localization:str = 'en_US'):
    self.bow:List[str] = bow
    self.fake:List[str] = Faker()

  def generate_name (self, n:int) -> List[str]:
    return [ self.fake.name() for _ in range(n) ]

  def generate_tokens (self, n:int) -> Set[str]:
    try:
      return self.fake.random_elements(elements=self.bow, length=n, unique=True)
    except ValueError as e:
      print (e)
      return None

  def generate_data (self, n:int, f_name:str='N', **kwargs) -> Any:
    # distribucion normal 
    if f_name == 'N':
      return np.random.normal(0, 1, n)
    # distribucion uniforme
    if f_name == 'U':
      try:
        return np.random.uniform(kwargs['a'], kwargs['b'], n)
      except Exception as e:
        print (e)
        return None
    
    

    return 



def to_visualizate ( data: np.array ) -> None:
  plt.hist(data, bins=30,density=True)
  plt.title('Histograma de datos')
  plt.xlabel('Valor')
  plt.ylabel('Frecuencia')
  plt.savefig(os.getcwd() + '/Data/Img/hist.png')



if __name__ == '__main__':
  dg = DataGenerator(bow=BOW_MUSIC)
  print(dg.generate_name(10))
  print(dg.generate_tokens(10))
  
  data = dg.generate_data(10)
  print (type(data))
  to_visualizate(data)

""" 

def random_choices ( n: int, tokens: list[ str ], length: int ) -> list[ str ]:
  fake = Faker ( )
  l = [ fake.random_choices ( elements=tokens, length=length ) for _ in range ( n ) ]
  return l

def random_digit ( n: int ) -> list [ int ]:
  fake = Faker ( )
  l = [ fake.random_digit ( ) for _ in range ( n ) ] 
  return l

def random_int ( n: int, lim_min: int, lim_max: int, step: int ) -> list[ int ]:
  fake = Faker ( )
  l = [ fake.random_int ( min=lim_min, max=lim_max, step=step ) for _ in range ( n ) ]
  return l 

def random_letter ( n: int, length: int ) -> str:
  fake = Faker ( )
  l = [ fake.random_letters ( length=length ) for _ in range ( n )  ]
  return l 

def random_elements ( n: int, tokens: list, length: int, unique_tokens: bool = True ) -> list[ str ]:
  fake = Faker ( )
  l = [ fake.random_elements ( elements=tokens, length=length, unique=unique_tokens ) for _ in range ( n ) ]
  return l 

def random_color ( n: int ) -> list [ str ]:
  fake = Faker ( )
  l = [ fake.safe_color_name ( ) for _ in range ( n ) ]
  return l 

def random_emoji ( n: int ) -> list [ str ]: 
  fake = Faker ( )
  l = [ fake.emoji ( ) for _ in range ( n ) ]
  return l

def random_jobs ( n: int ) -> list [ str ]:
  fake = Faker ( )
  l = [ fake.job ( ) for _ in range ( n ) ]
  return l 

def random_words ( n: int, localization: str ) -> list [ str ]:
  fake = Faker ( locale=localization )
  l = [ fake.word ( ) for _ in range ( n ) ]
  return l

def random_word_lists ( n: int, lenght: int ) -> list [ list [ str ] ] :
  fake = Faker ( )
  l = [ fake.words ( unique=True, nb=lenght ) for _ in range ( n ) ]
  return l


"""


