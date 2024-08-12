from typing import Any


class Printer_Arguments( object ):
  def __init__(self, f) -> None:
    self.f = f 
  def __call__(self, *args: Any, **kwds: Any) -> Any:
    print ( args )
    print ( kwds )
    value = self.f( *args, **kwds )
    return value



def printer_args ( f ):
  def func (*args, **kwargs):
    print( args )
    print( kwargs )
    return f( *args, **kwargs )
  return func

@printer_args
def special_sum ( array: list[int], boolean: bool, exponent: int ):
  value = sum(array)
  if boolean:
    return value**exponent
  return value





def main() -> None:
  print( '\n===============================================\n' )

  results = { }
  
  results[ 0 ] = special_sum( [i for i in range(0,10)], boolean=True, exponent=2 )
  results[ 1 ] = special_sum( [i*2 for i in range(0,10)], boolean=False, exponent=0 )

  print( f'\nRESULTS: {results}' )

  print( '\n===============================================\n' )

if __name__ == '__main__':
  main()