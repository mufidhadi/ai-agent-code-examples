from openai import OpenAI

client = OpenAI(
    base_url = 'http://localhost:11434/v1',
    api_key='ollama', # required, but unused
)

response = client.chat.completions.create(
  model="llama3.2:3b",
  messages=[
    {"role": "system", "content": "kamu adalah seorang pelawak yang suka bikin lawakan politik, kamu dikenal dengan nama fufufafa. kamu selalu menjawab pertanyaan dengan ledekan yang keratif dan sarkastik."},
    {"role": "user", "content": "kenapa jokowi menang pemilu presiden 2019?"},
  ]
)
print(response.choices[0].message.content)