import os
import dotenv

import asyncio

from typing import List 
from langchain_google_genai import GoogleGenerativeAI
from playwright.async_api import async_playwright

from langchain_community.document_loaders import AsyncChromiumLoader, AsyncHtmlLoader
from langchain_community.document_transformers.html2text import Html2TextTransformer
from langchain_community.document_transformers.beautiful_soup_transformer import BeautifulSoupTransformer
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, CommaSeparatedListOutputParser, JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

dotenv.load_dotenv()
google_api_key = os.getenv("google_api_key")

# SCRAPING
urls = [
  'https://uww.org/events'
]

# DEF MODEL
model = GoogleGenerativeAI(
  model='models/gemini-1.5-pro',
  temperature=0,
  google_api_key=google_api_key
)

def testing():
  loader = AsyncHtmlLoader(urls)
  docs = loader.load()

  html2text = Html2TextTransformer()
  docs_transformed = html2text.transform_documents(docs)


def scrape_with_playwright(urls):
  loader = AsyncChromiumLoader(urls)
  docs = loader.load()
  bs_transformer = BeautifulSoupTransformer()
  docs_transformed = bs_transformer.transform_documents(
    docs, tags_to_extract=['div']
  )

  for i in range(len(urls)):
    page_content = docs_transformed[i].page_content
    print(prompt_template(page_content))

async def scrape_with_playwright_and_years(urls, years):
  content_in_years = []
  async with async_playwright() as p:
    browser = await p.chromium.launch(headless=True)
    page = await browser.new_page()

    for year in years:
      await page.goto(urls[0])

      await page.evaluate( 
        ''' () => {
          document.getElement
        }

        ''' )

      content = await page.content()
      bs_transformer = BeautifulSoupTransformer()
      docs_transformed = bs_transformer.transform_documents(
        [content], tags_to_extract=['div'])
      content_in_years.append(docs_transformed)

    await browser.close()
  return content_in_years

def prompt_template(page_content):
  prompt = ChatPromptTemplate.from_messages([
    ("system", "Extrae informacion del siguiente contexto siguiente. Siguiendo este formato {format_instruction}"),
    ("human", "{context}")
  ])

  class Event(BaseModel):
    name: str = Field(description='Nombre del Torneo')
    date: str = Field(description='Fecha en la cual se desarrollo el Torneo')
    age: str = Field(description='Edad: puede ser Senior, U20, ..., U17')
    style: List[str] = Field(description='Puede ser FS, WW, GR')
  class Events(BaseModel):
    events: List[Event] = Field(description='Lista de todos los eventos desarrollados')

  parser = JsonOutputParser(pydantic_object=Events)
  chain = prompt|model|parser

  result = chain.invoke({
    "context": page_content,
    "format_instruction": parser.get_format_instructions()
  })

  return result

# scrape_with_playwright(urls)
async def main():
  await scrape_with_playwright_and_years(urls, ['2024', '2023'])

asyncio.run(main())