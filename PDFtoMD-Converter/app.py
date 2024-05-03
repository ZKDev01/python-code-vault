import os
import PyPDF2

# BASE
def convert_pdf_to_txt(pdf_path, txt_path):
  with open(pdf_path, 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    with open(txt_path, 'w') as output:
      for page in reader.pages:
        text = page.extract_text()
        output.write(text)

dir = os.getcwd() 

# Examples
dir_pdf = dir + '\\PDFtoMD-Converter\\database\\Julio Verne - Carpatos.pdf'
dir_txt = dir + '\\PDFtoMD-Converter\\database\\Julio Verne - Carpatos.txt'

convert_pdf_to_txt(dir_pdf, dir_txt)