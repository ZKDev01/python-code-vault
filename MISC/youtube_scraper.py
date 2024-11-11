import os
import time 
import http.client
import streamlit as st 

from pytube import YouTube

DIR = os.getcwd() + '\\videos'

def main ( ) -> None:
  st.write ('Streamlit Downloader')
  
  link = st.text_input("Introduce el enlace a descargar")
  btn = st.button("OK")
  if btn and link != "":
    yt = YouTube(link)
    st.write (f"Title: {yt.title}")
    st.write (f"View: {yt.views}")
    st.write (f"Description {yt.description}")

    #streams = yt.streams.get_highest_resolution()
  
  
if __name__ == '__main__':
  main ( )
