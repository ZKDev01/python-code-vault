import string as s 
import random as r 
import streamlit as st 

st.title ("Password Generator")



total = s.ascii_lowercase + s.ascii_uppercase + s.digits + s.punctuation 


def main() -> None:
  length = st.number_input ( 
    label='Select password length',
    min_value=4,
    max_value=50
  )
  password = "".join( r.sample(total,length) )
  st.write (password)


if __name__ == "__main__":
  main()