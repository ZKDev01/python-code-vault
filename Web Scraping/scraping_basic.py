import requests
import streamlit as st 

from bs4 import BeautifulSoup

st.title ("Simple Web Scraping")


url = st.text_input (
  label='Insert URL'
)
opt = st.multiselect (
  label='Select the scraping-options',
  options=[ 'extract imgs', 'extract links', 'extract paragraphs' ]
)

btn = st.button(
  label='Start scraping'
)

if btn:
  try:
    response = requests.get(url=url)
    soup = BeautifulSoup(response.content, 'html.parser')
  except Exception as e:
    st.write (e)

  if 'extract imgs' in opt:
    st.write ("init extract imgs")
  
  if 'extract links' in opt:
    st.write ("init extract links")

  if 'extract paragraphs' in opt:
    st.write ('extract paragraphs')


