import os
import dotenv

from langchain_google_genai import GoogleGenerativeAI

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, CommaSeparatedListOutputParser, JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

dotenv.load_dotenv()
google_api_key = os.getenv("geminiapi_key")

model = GoogleGenerativeAI(
  model='gemini-pro',
  google_api_key=google_api_key)

def basic_invoke():
  result = model.invoke("Que relacion existe entre el machine learning y la inteligencia artificial")
  print(result)

def prompt_template_basic():
  prompt = ChatPromptTemplate.from_template("Desarrollame un algoritmo en python que permita {algoritmo}")
  chain = prompt | model
  result = chain.invoke({"algoritmo": "dado un arreglo de numeros, obtener la suma de sus cuadrados"})
  print(result)

def prompt_template_messages_in_system():
  prompt = ChatPromptTemplate.from_messages(
    [ 
      ("system", "Eres una inteligencia artificial que solo devuelve 10 sinonimos de una palabra que el humano introduzca"),
      ("human", "{input}")
    ]
  )

  chain = prompt | model 
  result = chain.invoke({"input": "Proactivo"})
  print(result)

def parser_simple_string():
  prompt = ChatPromptTemplate.from_template("Dime 10 sinonimos de: {input}")
  parser = StrOutputParser()

  chain = prompt | model | parser
  result = chain.invoke({"input": "Persona"})
  
  print(result)

def parser_simple_list():
  prompt = ChatPromptTemplate.from_template("Dime 10 sinonimos de: {input} y los sinonimos quiero que esten separados por coma")
  parser = CommaSeparatedListOutputParser()

  chain = prompt | model | parser
  result = chain.invoke({"input": "Persona"})
  
  print(result)

def parser_simple_json():
  prompt = ChatPromptTemplate.from_messages([
    ("system", "Extrae informacion de la siguiente frase. Siguiendo este formato {format_instructions}"),
    ("human", "{input}")
  ])

  class Person(BaseModel):
    name: str = Field(description="nombre de la persona")
    age: int = Field(description="edad de la persona")

  parser = JsonOutputParser(pydantic_object=Person)
  chain = prompt | model | parser

  result = chain.invoke({
    "input": "Raimel y tengo 22 años",
    "format_instructions": parser.get_format_instructions()
  })
  print(result)

def prompt_template_basic_sport(url = 'https://uww.org/events'):
  result = model.invoke(f"Que eventos ocurrieron en este url en el año 2020 {url}")
  print(result)

if __name__ == "__main__":
  prompt_template_basic_sport()