import dotenv
import os

from langchain_google_genai import GoogleGenerativeAI

dotenv.load_dotenv()

os.environ.setdefault('google_api_key', os.getenv('google_api_key')) 

model = GoogleGenerativeAI(
  model='models/gemini-1.5-pro'
)

def basic_invoke():
  result = model.invoke("Que relacion existe entre el machine learning y la inteligencia artificial")
  print(result)

if __name__ == '__main__':
  basic_invoke()