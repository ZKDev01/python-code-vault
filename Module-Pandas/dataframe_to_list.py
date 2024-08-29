
import pandas as pd 


def test_1 ( ) -> None:
  


  df = pd.DataFrame ( { 
    'A': [ 1, 3, 5 ], 
    'B': [ 2, 4, 6 ] }
  )
  list_df = df.values.tolist ()

  print ( 'DATAFRAME' )
  print ( df )

  print ( 'LIST' )
  print ( list_df )




if __name__ == '__main__':
  test_1 ()