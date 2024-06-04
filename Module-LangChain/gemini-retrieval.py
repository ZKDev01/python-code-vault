import os
from typing import List
import dotenv

from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings

from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

dotenv.load_dotenv()
google_api_key = os.getenv("geminiapi_key")

model = GoogleGenerativeAI(
  model='models/gemini-1.5-pro',
  google_api_key=google_api_key)
embedding = GoogleGenerativeAIEmbeddings(
  model='models/embedding-001',
  google_api_key=google_api_key
)

def load_doc(dir: str):
  loader = PyPDFLoader(dir)
  docs = loader.load()

  splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=20
  )

  docs = splitter.split_documents(docs)

  return docs[1::10]

def embedding_doc(docs: List[Document]):
  pass

if __name__ == "__main__":
  current = os.getcwd()
  dir = '\\Module-LangChain\\database\\results_02_acapulco.pdf'
  first = load_doc(current + dir)
  for doc in first:
    print(doc.page_content)



