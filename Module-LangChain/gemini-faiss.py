import os 
import dotenv

from langchain_community.document_loaders import TextLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings, GoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.faiss import FAISS

dotenv.load_dotenv()
google_api_key = os.getenv('google_api_key')

model = GoogleGenerativeAI(
  model='models/gemini-1.5-pro',
  google_api_key=google_api_key
)
embedding = GoogleGenerativeAIEmbeddings(
  model='models/embedding-001',
  google_api_key=google_api_key
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

if __name__ == '__main__':
  current = os.getcwd()
  dir = '\\Module-LangChain\\database\\testing.txt'
  docs = load_doc(current + dir)
  db = FAISS.from_documents(docs, embedding)
  query = "Cual es el perro de Persona 1?"
  results = db.similarity_search(query)
  print(results)
