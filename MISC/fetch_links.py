import requests as rq 
from bs4 import BeautifulSoup

url = ''

if ('https' or 'http') in url:
  data = rq.get(url)
else:
  raise Exception (f"not found url {url}")

soup = BeautifulSoup(data.text, "html.parser")
links = [ ]

for link in soup.find_all('a'):
  links.append(link.get('href'))

for i, item in enumerate(links):
  print (f"{i}. {item}")
