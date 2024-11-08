import os
import PyPDF2

def convert_pdf_to_txt(pdf_path, txt_path):
  """
  
  """
  with open(pdf_path, 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    with open(txt_path, 'w', encoding='utf-8') as output:
      for page in reader.pages:
        text = page.extract_text()
        output.write(text)

def convert_pdf_to_md(pdf_path, md_path):
  """
  
  """
  with open(pdf_path, 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
      text += page.extract_text()
  lines = text.split('\n')
  md_text = ""
  for line in lines: 
    line = line.strip()
    if line == "":
      md_text += "\n\n"
    else:
      md_text += line + "\n"
  with open(md_path, 'w', encoding='utf-8') as output:
    output.write(md_text)

dir = os.getcwd() 

# Examples
dir_pdf = 'database/publicacion_24.pdf'
dir_txt = 'database/publicacion_24.txt'
dir_md  = 'database/publicacion_24.md' 

convert_pdf_to_txt(dir_pdf, dir_md)
