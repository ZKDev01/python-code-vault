import os
import fnmatch
import pandas as pd 
import requests
import csv
from bs4 import BeautifulSoup

url = 'https://es.wikipedia.org/wiki/Campeonato_Mundial_de_Lucha_de_2023'

def extract_tables_from_html(url: str):
  response = requests.get(url)
  if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all('table')
    tables = [table for table in tables]
    html_files = []
    for i, table in enumerate(tables, start=1):
      file_name = 'index_{}.html'.format(i)
      with open(file_name, 'w', encoding='utf-8') as file:
        file.write(table.prettify())
      html_files.append(file_name)
  else:
    print("Error al acceder a {}: {}".format(url, response.status_code))

def convert_csv_from_html(dir: str):
  for dirpath, dirs, files in os.walk(dir):
    for filename in fnmatch.filter(files, '*.html'):
      full = os.path.join(dirpath, filename)
      with open(full, 'r', encoding='utf-8') as f:
        html = f.read()
        soup = BeautifulSoup(html, 'html.parser')
        tables = soup.find_all('table')
        name_csv = os.path.splitext(filename)[0] + '.csv'
        with open(name_csv, 'w', newline='', encoding='utf-8') as f_csv:
          writer = csv.writer(f_csv)
          for table in tables:
            rows = table.find_all('tr')
            for row in rows:
              columns = row.find_all('td')
              if columns:
                writer.writerow([c.text.split() for c in columns])

if __name__ == "__main__":
  extract_tables_from_html(url)
  dir = os.getcwd()
  convert_csv_from_html(dir)