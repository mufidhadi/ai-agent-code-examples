from openai import OpenAI
from qdrant_client import QdrantClient
from dotenv import load_dotenv
import os

load_dotenv()

collection_name = 'faq_chatbot'
embedding_size = 384
rag_treshold = 0.65

query = "gimana cara login di aplikasi?"

print(query)

client_q = QdrantClient(host='10.120.10.1', port=6333)
try:
    existing_collection =  client_q.get_collection(collection_name=collection_name)
except:
    existing_collection = client_q.create_collection(collection_name=collection_name, vectors_config={'size': embedding_size, 'distance': 'Cosine'})
# print(existing_collection)

client = OpenAI(
    base_url = 'http://localhost:11434/v1',
    api_key='ollama', # required, but unused
)

client2 = OpenAI(
    api_key=os.getenv('GOOGLE_API_KEY','ollama'),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.embeddings.create(
    input=query,
    model="all-minilm:latest"
)

embedding = response.data[0].embedding
# print(len(embedding))
embedding_size = len(embedding)

response = client_q.query_points(
    collection_name=collection_name,
    query=embedding,
    limit=5
)
# print(response)

retrived_context = [{
    'score': p.score,
    **p.payload
} for p in response.points if p.score > rag_treshold]

# print(retrived_context)

rag_context = '- '+'\n- '.join([c['content'] for c in retrived_context])

print(rag_context)

message = [{'role':'system', 'content':'you are a helpful assitant'}]
message.append({
    'role':'user',
    'content':query
})
message.append({
    'role':'system',
    'content':'Retrieved context: \n'+rag_context
})

response = client2.chat.completions.create(
#   model="mistral:7b",
  model="gemini-2.0-flash",
  messages=message
)

print('---')
print(response.choices[0].message.content)
