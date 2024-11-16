import streamlit as st 

class TestComponent:
  def __init__(self, word: str, n: int = 10) -> None:
    self.word = word
    self.n = n

  def display_word ( self ) -> None:
    for i in range ( self.n ):
      st.write ( f'{i+1}. {self.word}' )
    
  def calculate ( self, m: int ) -> None:
    r = self.n ** m
    st.write ( f'RESULT: {r}' ) 



def main ( ) -> None:
  text = st.text_input ( 'Enter a text' )
  value = st.number_input ( 'Enter a number', min_value=0 )

  s_btn = st.button ( 'SUBMIT' )
  if s_btn:
    test_component = TestComponent( word=text, n=value ) 
    st.button ( 'DISPLAY WORD', on_click=test_component.display_word )

    s_btn_2 = st.button ( 'another widget' )
    if s_btn_2:
      another_value = st.number_input ( 'Enter a number', min_value=0 )
      st.button ( 'CALCULATE', on_click=test_component.calculate, args=(another_value,) )



if __name__ == '__main__':
  main ( )
