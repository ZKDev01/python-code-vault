import os
import json
import streamlit as st 

JSON_FILE = 'input.json'
DIR_JSON = os.getcwd() + '/_data/' + JSON_FILE


st.title ("Json File to CSV File")
st.markdown ("""
This script
""")

# TODO: Drag and copy + functional script

def main ( ) -> None:
  try:
    with open(DIR_JSON, 'r') as f:
      data = json.loads ( f.read() )
      st.write (data)
  except Exception as e:
    st.write (f'dont found: {DIR_JSON}')
    

if __name__ == '__main__':
  
  main ( )


