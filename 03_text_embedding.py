from openai import OpenAI

client = OpenAI(
    base_url = 'http://localhost:11434/v1',
    api_key='ollama', # required, but unused
)

response = client.embeddings.create(
    input="ubur-ubur ikan lele, kapan emyu menang le?",
    model="all-minilm:latest"
)

print(response.data[0].embedding)