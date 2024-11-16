from pymongo import MongoClient

client = MongoClient('localhost')
db = client['embedding_document_database'] 

collection = db['vector']

def add():
  collection.insert_one({
    'element1': 10,
    'element2': '1'
  })
  # exist 'insert_many'

print(db.list_collection_names())
print(client.list_database_names())