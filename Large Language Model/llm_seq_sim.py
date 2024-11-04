import os
import dotenv

from langchain_core.documents import Document
from langchain_community.vectorstores.faiss import FAISS
from langchain_google_genai import GoogleGenerativeAI,GoogleGenerativeAIEmbeddings

dotenv.load_dotenv()
os.environ.setdefault ('google_api_key', os.getenv('google_api_key'))

model = GoogleGenerativeAI(
  model='models/gemini-1.5-pro',
  temperature=0.6
)
embedding = GoogleGenerativeAIEmbeddings(
  model='models/embedding-001'
)

documents = [
  Document(page_content="Este es el primer documento."),
  Document(page_content="Este es el segundo documento."),
  Document(page_content="Este es el tercer documento.")
]

dimension = len(next(iter(documents)).page_content)

FAISS.sim

print (dimension)


"""

index = faiss.IndexFlatL2(dimension)

for i, doc in enumerate(documents):
    vec = gemini_model.embed(doc.content)
    index.add(vec.reshape(1, -1))

def calculate_seq_simil(doc1, doc2, window_size=5):
    seq_simil = 0
    min_len = min(len(doc1), len(doc2))
    
    for i in range(min_len):
        window_start = max(0, i - window_size + 1)
        window_end = min(i + window_size + 1, min_len)
        
        seq_simil += sum(gemini_model.similarity(doc1[window_start:i+1], doc2[i-window_size+1:i+1]))
    
    return seq_simil / (min_len * 2 * window_size)


def sequential_similarity_search(query_doc, top_k=3):
    query_vec = gemini_model.embed(query_doc.content)
    distances, indices = index.search(query_vec.reshape(1, -1), top_k)
    
    similar_docs = []
    for idx in indices[0]:
        similar_docs.append(documents[idx])
    
    return sorted(similar_docs, key=lambda x: calculate_seq_simil(x, query_doc), reverse=True)


query = Document(content="Este es un ejemplo de consulta.")
results = sequential_similarity_search(query)

print("Resultados similares:")
for doc in results[:3]:
    print(doc.content)
"""