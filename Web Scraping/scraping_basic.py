import requests
import streamlit as st 

from bs4 import BeautifulSoup

st.title ("Simple Web Scraping")

# region: Work with BS
def extract_imgs (soup:BeautifulSoup):
  #TODO Mejorar la obtencion de imagenes 
  imgs = [ img.get('src') for img in soup.find_all('img') ]
  return imgs

def extract_links (soup:BeautifulSoup):
  links = [ link.get('href') for link in soup.find_all('a')]
  return links

def extract_paragraphs (soup:BeautifulSoup):
  paragraphs = soup.find_all('p')
  return paragraphs
# endregion


# def scraping-options 
options = {
  'extract imgs'       : extract_imgs,
  'extract links'      : extract_links,
  'extract paragraphs' : extract_paragraphs
}

url = st.text_input (
  label='Insert URL'
)
opt = st.multiselect (
  label='Select the scraping-options',
  options=options.keys()
)
btn = st.button(
  label='Start scraping'
)


if btn:
  try:
    response = requests.get(url=url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    for o in opt:
      func = options.get(o)
      result = func(soup=soup)
      st.write (result)
  
  except Exception as e:
    st.write (e)



