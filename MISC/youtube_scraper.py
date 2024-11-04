import os
import time 
import http.client
from pytube import YouTube

dir = os.getcwd() + "\\YT-Scraper\\database"

link = ""
yt = YouTube(link)

print("Title: ", yt.title)
print("View: ", yt.views)

yt_highest = yt.streams.get_highest_resolution()
yt_lowest = yt.streams.get_lowest_resolution()

for attempt in range(3):
  print("Iniciando Descarga")
  try: 
    yt_lowest.download(dir)
    print("Descarga exitosa")
    break
  except http.client.IncompleteRead as e:
    print("Error en la descarga (intento {}):".format(attempt + 1))
    time.sleep(3)

