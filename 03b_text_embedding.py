from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv('GOOGLE_API_KEY','ollama'),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.embeddings.create(
    input="ubur-ubur ikan lele, kapan emyu menang le?",
    model="text-embedding-004"
)

print(response.data[0].embedding)