from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv('GOOGLE_API_KEY','ollama'),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
  model="gemini-2.0-flash",
  messages=[
    {"role": "system", "content": "kamu adalah seorang pelawak yang suka bikin lawakan politik, kamu dikenal dengan nama fufufafa. kamu selalu menjawab pertanyaan dengan ledekan yang keratif dan sarkastik."},
    {"role": "user", "content": "kenapa jokowi menang pemilu presiden 2019?"},
  ]
)
print(response.choices[0].message.content)