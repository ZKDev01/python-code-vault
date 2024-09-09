import streamlit as st

from faker import Faker
from faker.providers import DynamicProvider

WORD_LIST = [ 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', '...', 'x', 'y', 'z' ]



def generator_name_list ( n: int, localization: str = 'en_US' ) -> list[ str ]:
  # possible locales: [ en_US, it_IT, ja_JP, es_ES, ... ]
  fake = Faker ( locale=localization )
  l = [ ]
  for _ in range ( 0, n ):
    l.append ( fake.name ( ) )
  return l


def generator_tokens_unique_list ( n: int, word_list: list[ str ] ) -> list[ str ]:
  fake = Faker ( )
  tokens = [ ]
  for _ in range ( 0, n ):
    tmp = [ word for word in word_list if word is not tokens ]
    s = fake.sentence ( nb_words=1, ext_word_list=tmp )
    tokens.append ( s[0:len(s)-1] )
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
    names = generator_name_list ( n=n )
    tokens = generator_tokens_unique_list ( n=n, word_list=WORD_LIST )
    paragraphs = random_words ( n=n, localization='es_ES' )
    word_lists = random_word_lists ( n=n, lenght=5 )

    for i, name in enumerate( names ):
      st.write ( f"{ i+1 }. Name: { name }" )

    for i, tk in enumerate( tokens ):
      st.write ( f"Token { i+1 } => { tk }" )

    st.write ( 'PARAGRAPH' )
    for p in paragraphs: 
      st.write ( p )

    st.write ( 'WORD LISTS' )
    for l in word_lists:
      st.write ( l )




if __name__ == '__main__':
  deploy ( )
