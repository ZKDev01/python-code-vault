import streamlit as st

from faker import Faker
from faker.providers import DynamicProvider

WORD_LIST = [
  'action',
  'comedy',
  'drama',
  'horror',
  'fantasy',
  'jazz',
  'rock',
  'pop',
  'classical',
  'hip-hop'
]



def generator_name_list ( n: int, localization: str = 'en_US' ) -> list[ str ]:
  # possible locales: [ en_US, it_IT, ja_JP, es_ES, ... ]
  fake = Faker ( locale=localization )
  l = [ ]
  for _ in range ( 0, n ):
    l.append ( fake.name ( ) )
  return l


def generator_tokens_unique_list ( word_list: set[ str ], n: int = -1 ) -> set [ str ]:
  fake = Faker ( )

  if n == -1:
    n = fake.random_int ( min=0, max=len(word_list)-1 )

  tokens = fake.random_elements ( elements=word_list, length=n, unique=True )
  return tokens





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


def deploy ( ) -> None:
  n = st.slider ( 'Select a range of values', 0, 10, 0 )
  
  if n:
    tokens = generator_tokens_unique_list ( word_list=WORD_LIST )

    
    st.write ( tokens ) 





if __name__ == '__main__':
  deploy ( )
