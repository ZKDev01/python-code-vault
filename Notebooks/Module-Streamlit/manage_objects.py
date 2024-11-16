import streamlit as st 

from typing import Any, List

class Metadata:
  def __init__(self, name: str, value: Any) -> None:
    self.name = name
    self._value = value
    self.type_value = type ( value )
  
  def set_value ( self, value: Any ) -> None:
    if type( value ) == self.type_value:
      self._value = value
    else: raise Exception ( 'Error Type' )

  def get_value ( self ) -> Any:
    return self._value

class Node: 
  def __init__(self, id: int, name: str, metadatas: List[ Metadata ]) -> None:
    self._id = id
    self.name = name
    self.metadatas = metadatas

  def __str__(self) -> str:
    return f'<{self._id}> {self.name}'



def main ( ) -> None:
  st.set_page_config ( layout='wide' )

  column_1, _, column_2 = st.columns( [2,1,2] )

  st.header ( 'Input' )
  st.session_state.node = None
  st.session_state.metadatas_list = [ ]

  with column_1:
    id_number = st.number_input ( 'ID:', key='ID', min_value=0, max_value=100 )
    name_node = st.text_input ( 'Name:', key='Name-Node' )
    metadatas = [ ]
    if not st.session_state.metadatas_list == [ ]: 
      metadatas = st.multiselect( 'Metadatas', st.session_state.metadatas_list )
    if st.button ( 'Create' ):
      st.session_state.node = Node ( id=id_number, name=name_node, metadatas=metadatas )
  
  with column_2:
    metadata_name = st.text_input ( 'Metadata Name' )
    metadata_value = st.text_input ( 'Metadata Value' )
    if st.button ( 'Create Metadata' ):
      st.session_state.metadatas_list.append ( Metadata ( name=metadata_name, value=metadata_value ) )

  st.header ( 'Output' )
  if not st.session_state.node == None:
    st.write ( f'[{st.session_state.node._id}] {st.session_state.node.name}' )



if __name__ == '__main__':
  main ( )