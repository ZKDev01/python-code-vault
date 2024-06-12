import os
import dotenv

from langchain_google_genai import GoogleGenerativeAI

def load_environment():
  """
  Carga las variables de entorno necesarias para el funcionamiento del programa

  Esta funcion utiliza la biblioteca `dotenv` para cargar variables de entorno desde un archivo `.env`

  Especificamente buscar las variables de entorno siguientes:
  - `google_api_key` : clave de API de Google  
  """

  dotenv.load_dotenv()
  os.environ.setdefault('google_api_key', os.getenv('google_api_key'))

def get_model() -> GoogleGenerativeAI:
  """
  Inicializa y devuelve una instancia de GoogleGenerativeAI
  con configuraciones predeterminadas 

  Contiene una funcion para cargar las credenciales de Google API 
  desde el entorno y crea una instancia de GoogleGenerativeAI
  usando el modelo 'gemini-1.5-pro'

  Args:

  Returns:
      GoogleGenerativeAI: instancia preconfigurada de GoogleGenerativeAI
  """
  
  load_environment()
  model = GoogleGenerativeAI(
    model='models/gemini-1.5-pro'
  )
  return model

def get_embedding():
  pass