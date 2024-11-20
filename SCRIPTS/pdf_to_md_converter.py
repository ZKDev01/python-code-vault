import os
import io 
import base64
import PyPDF2
import streamlit as st 
from PIL import Image


PATH = os.getcwd() + '/_data/'
DOCUMENT = 'experimental-functions.pdf' 


def pdf2md():
  try:

    with open (PATH + DOCUMENT, 'rb') as file:
      reader = PyPDF2.PdfReader(file)
      text = dict()
      images = [ ]

      for i, page in enumerate( reader.pages ):
        text[i] = page.extract_text()
        tmp = """
  
        for image in page.images:
          image_data = io.BytesIO(image.data)

          image_base64 = base64.b64encode( image_data.getvalue() ).decode('utf-8')
          
          tmp_image_path = f'tmp_{len(images)+1}.png'
          with open(tmp_image_path, 'wb') as tmp_file:
            tmp_file.write (image_data.getvalue())

          image_path = f"![]({tmp_image_path})"
          images.append( image_path )

  Returns:
      _type_: _description_
        """
    
      return text, images

  except Exception as e:
    st.write ("fail to converter pdf file")
    with st.expander( "Error", expanded=False ):
      st.write (e)



def main ( ) -> None:
  st.title ("pdf2markdown Converter")

  markdown, images = pdf2md()
  st.markdown ( PATH+DOCUMENT )

  for i, page in markdown.items():
    st.write (f'### Page {i}')
    st.write (page)
  # TODO mostrar el pdf original 
  
  # TODO mostrar el markdown convertido 



if __name__ == '__main__':
  main ( )
