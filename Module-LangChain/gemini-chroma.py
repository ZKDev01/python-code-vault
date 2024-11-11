import dotenv
import os

from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

from langchain_community.vectorstores import Chroma 

dotenv.load_dotenv()

os.environ.setdefault('google_api_key', os.getenv('google_api_key')) 

model = GoogleGenerativeAI(
  model='models/gemini-1.5-pro'
)
embedding = GoogleGenerativeAIEmbeddings(
  model='models/embedding-001'
)

def load_doc(dir: str):
  loader = TextLoader(dir)
  docs = loader.load()
  
  splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=20
  )
  docs = splitter.split_documents(docs)
  return docs

def main():
  # TODO: PROBLEMA CON Chroma.from_documents
  current = os.getcwd()
  dir = '\\Module-LangChain\\database\\testing.txt'
  docs = load_doc(current + dir)

  vectorstore = Chroma.from_documents(
    documents=docs, 
    embedding=embedding, 
    persist_directory='database')

  query = "Cual es el perro de Persona 1?"
  similary_score = vectorstore.similarity_search_with_score(query)
  print(similary_score)

if __name__ == '__main__':
  main()