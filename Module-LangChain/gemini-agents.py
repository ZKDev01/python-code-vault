import dotenv
import os

from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import tool

dotenv.load_dotenv()
os.environ.setdefault('google_api_key', os.getenv('google_api_key'))

model = GoogleGenerativeAI(
  model='models/gemini-1.5-pro'
)
embedding = GoogleGenerativeAIEmbeddings(
  model='models/embedding-001'
)

def make_prompts():
  prompt = ChatPromptTemplate.from_messages(
    [
      (
        "system",
        "You are very powerful assistant, but don't know current events"
      ),
      ("user", "{input}"),
      MessagesPlaceholder(variable_name="agent_scratchpad")
    ]
  )
  pass

def make_tools():
  tools = []
  
  @tool
  def get_word_length(word: str) -> int:
    """Returns the length of a word"""
    return len(word)

  tools.append(get_word_length)
  return tools 

def main():
  tools = make_tools()
  func = tools[0]

  result = func.invoke("abc")
  print(result)

if __name__ == '__main__':
  main()