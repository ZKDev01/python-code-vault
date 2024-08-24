import pandas as pd  
import random 

from typing import Any



def get_new_random_dataframe ( df: pd.DataFrame ) -> pd.DataFrame:
  n = len ( df )
  indexs = [ i for i in range ( 0, n ) ]
  

  for index, row in enumerate ( df.itertuples(), start=0 ):
    print ( f'Index: { index }' )
    print ( f'Tuple: {  row  }' )
  
  pass

def search_index ( df: pd.DataFrame, index: int ) -> Any:
  results = df.loc [ index ]
  print ( results )
  print ( type ( results ) )

def change_rows ( df: pd.DataFrame, index_i: int, index_j: int ) -> pd.DataFrame:
  copy_df = df.copy ()

  df.loc [ df.index [ index_i ], : ] = copy_df.loc [ df.index[ index_j ], : ]
  df.loc [ df.index [ index_j ], : ] = copy_df.loc [ df.index[ index_i ], : ]

  print ( df )

def test ( ) -> None:
  items = { 
    'Column-1' : [  1,  2,  3,  4 ],
    'Column-2' : [ 11, 12, 13, 14 ],
    'Column-3' : [ 21, 22, 23, 24 ],
    'Column-4' : [ 31, 32, 33, 34 ],
  }
  df = pd.DataFrame ( items )
  print ( df )

  #search_index ( df, index=0 )
  #search_index ( df, index=1 )
  #search_index ( df, index=3 )

  #change_rows ( df, 0, 1 )
  get_new_random_dataframe ( df )

def main ( ) -> None:
  pass


if __name__ == '__main__':
  print ( '\n=============== Print tests ===============\n' )
  test ( )

  print ( '\n========== Execute main function ==========\n' )
  main ( )

