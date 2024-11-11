from typing import List
import dotenv
import os

from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.documents import Document
from langchain.tools.retriever import create_retriever_tool
from langchain.agents import create_react_agent, AgentExecutor

dotenv.load_dotenv()
os.environ.setdefault('google_api_key', os.getenv('google_api_key'))
# tavily_api_key = os.getenv('tavily_api_key')

model = GoogleGenerativeAI(
  model='models/gemini-1.5-pro'
)
embedding = GoogleGenerativeAIEmbeddings(
  model='models/embedding-001'
)

def get_the_article() -> List[Document]:
  article_path = os.getcwd() + '\\Module-LangChain\\database\\Martin George R R - Cancion De Hielo Y Fuego 01 - Juego de Tronos.pdf'
  loader = PyPDFLoader(article_path)
  docs = loader.load_and_split()
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
  docs = text_splitter.split_documents(docs)
  return docs

def save_the_chunks_to_the_vector_database(docs: List[Document]) -> FAISS:
  vector = FAISS.from_documents(documents=docs[0:100], embedding=embedding)
  return vector

def create_retriever(vector: FAISS):
  retriever = vector.as_retriever()
  return retriever

def create_tools_retriever(retriever):
  tool_search_in_got_books = create_retriever_tool(
    retriever=retriever, 
    name='game_of_throne_search',
    description='Search for information about Game of Thrones'
  )

  tools = [tool_search_in_got_books]
  return tools

def main():
  docs = get_the_article()
  vector = save_the_chunks_to_the_vector_database(docs=docs)
  retriever = create_retriever(vector=vector)
  tools = create_tools_retriever(retriever=retriever)
  prompt = """
  Responde siguiendo las preguntas de la mejor forma posible. Tu puedes usar las siguientes herramientas:
  
  {tools}

  Usa el siguiente formato:

  Question: the input question you must answer
  Thought: you should always think about what to do
  Action: the action to take, should be one of [{tool_names}]
  Action Input: the input to the action
  Observation: the result of the action
  ... (este Thought/Action/Action Input/Observation puede repetirse N veces)
  Thought: ahora puedo saber mi respuesta final
  Final Answer: la respuesta final a la pregunta original (Question)

  Begin!

  Question: {input}
  Thought: {agent_scratchpad}
  """
  agent = create_react_agent(llm=model, tools=tools, prompt=prompt)
  agent_executer = AgentExecutor(agent=agent, tools=tools, verbose=True)

  agent_executer.invoke({'input':'quien es anya stark?'})

if __name__ == '__main__':
  main()