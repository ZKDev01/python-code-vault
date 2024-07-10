import dotenv
import os

from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

dotenv.load_dotenv()
os.environ.setdefault('google_api_key', os.getenv('google_api_key'))

model = GoogleGenerativeAI(
  model='models/gemini-1.5-pro'
)
embedding = GoogleGenerativeAIEmbeddings(
  model='models/embedding-001'
)

def simple_message_with_HumanMessage():
  model.invoke([HumanMessage(content="Hi! I'm a student")])
  # AIMessage(content = "Hello! How can I assist you today?")

def simple_chat():
  chat_history = []
  prompt = ChatPromptTemplate.from_messages(
    [(
        "system",
        """
        Eres un AI, respondes preguntas solo sobre problemas de optimizacion,
        ademas debes preguntar al usuario acorde al contexto

        los problemas de optimizacion son:
        {optimizacion}

        algunos ejemplos son:
        {problem_1}
        {problem_2}
        """
      ),
      MessagesPlaceholder(variable_name='chat_history'),
      ("human", "{input}")
    ])
  chain = prompt | model

  # CHAT
  while True:
    question = input("You: ")
    response = chain.invoke({"input": question, 'chat_history': chat_history})
    chat_history.append(HumanMessage(content=question))
    chat_history.append(AIMessage(content=response))

    print(f"{response}")

def main():
  simple_chat()

if __name__ == '__main__':
  main()