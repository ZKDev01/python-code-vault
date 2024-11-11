from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.llm import LLMChain
from langchain.chains.sequential import SequentialChain
from langchain.prompts import PromptTemplate

import streamlit as st

from personal_tool import get_model

model = get_model()

template_1 = """ 
I have a problem for you to solve, the problem is {input}
Provide {number} distinct solutions and I want you to take into consideration, factors such as {factors}
"""
prompt_1 = PromptTemplate(
  input_variables=["input", "factors", "number"],
  template=template_1
)
chain_1 = LLMChain(
  llm=model,
  prompt=prompt_1,
  output_key='prop_soln'
) 

template_2 = """
For each of the proposed solution, evaluate their potential 
Consider their pros and cons, initial effort required, implementation, difficulty, potential callenges, and the expected outcomes
Assign a probability of success and a confidence level to each option based on their factors
{prop_soln}
"""
prompt_2 = PromptTemplate(
  input_variables=["prop_soln"],
  template=template_2
)
chain_2 = LLMChain(
  llm=model,
  prompt=prompt_2,
  output_key='solns'
) 

template_3 = """
For each solution, elaborate on the thought process by generating potential scenarios, outlining strategies for implementation, 
identifying necesary partnership or resources, and proposing solutions to potential obstacles.
Additionally, consider any unexpected outcomes and outline contingency plans for their managment
{solns}
"""
prompt_3 = PromptTemplate(
  input_variables=["solns"],
  template=template_3
)
chain_3 = LLMChain(
  llm=model,
  prompt=prompt_3,
  output_key='proc_output'
) 

template_4 = """
Rank the solutions based on evaluations and scenarios, assigning a probability of sucess in percentage for each.
Provide justification and final thought for each ranking.
Each ranking should be broken down into 4 points, Probability of sucess, justification, modes of failure and final thoughts. 
Rank according to the highest probability of sucess
{proc_output}
"""
prompt_4 = PromptTemplate(
  input_variables=["proc_output"],
  template=template_4
)
chain_4 = LLMChain(
  llm=model,
  prompt=prompt_4,
  output_key='result'
) 

chain = SequentialChain(
  chains=[chain_1,chain_2,chain_3,chain_4],
  input_variables=["input", "factors", "number"],
  output_variables=['result']
)

st.header("Gemini ToT")

inp = st.text_input("Input", placeholder="Input", label_visibility='visible')
factors = st.text_input("Factors concerning the input", placeholder="Factors", label_visibility='visible')
num = st.slider("How many distinct solutions do you want ?", 2, 5, step=1)

if st.button("PROCESS", use_container_width=True):
  res = chain({"input": inp, "factors": factors, "number": num})
  st.write("")
  st.write(":blue[Response]")
  st.write("")

  st.markdown(res['result'])

