from openai import OpenAI
import json
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv('GOOGLE_API_KEY','ollama'),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current temperature for a given location.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and country e.g. jakarta, indonesia"
                }
            },
            "required": [
                "location"
            ],
            "additionalProperties": False
        }
    }
}]

def get_weather(location):
    return f"the temperature in {location} is 28 degrees celcius"

messages = [{"role": "user", "content": "suhu di jakarta sekarang seberapa?"}]
response = client.chat.completions.create(
  model="gemini-2.0-flash",
  messages=messages,
  tools=tools,
  tool_choice="auto"
)

if response.choices[0].finish_reason == "tool_calls":
    messages.append(response.choices[0].message)
    for tool in response.choices[0].message.tool_calls:
        tool_name = tool.function.name
        tool_args = tool.function.arguments
        tool_args = json.loads(tool_args)
        tool_output = globals()[tool_name](**tool_args)
        messages.append({"role": "function", "name": tool_name, "content": tool_output})
    response = client.chat.completions.create(
        model="gemini-2.0-flash",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
print(response.choices[0].message.content)