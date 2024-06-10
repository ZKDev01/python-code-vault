import dotenv
import os

from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores.faiss import FAISS

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
  current = os.getcwd()
  dir = '\\Module-LangChain\\database\\testing.txt'
  docs = load_doc(current + dir)
  db = FAISS.from_documents(documents=docs, embedding=embedding)
  query = "Cual es el perro de Persona 1?"
  results = db.similarity_search(query, k=1)
  for result in results:
    print(f"PAGE CONTENT: {result.page_content}")
    print(f"METADATOS: {result.metadata}")

if __name__ == '__main__':
  main()