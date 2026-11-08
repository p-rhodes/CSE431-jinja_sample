#This is a test script so I can try out a free llm api since I no have the
#money for the claude api

import os
from openai import OpenAI

if not os.getenv("GROQ_API_KEY"):
    raise SystemExit("No api key!")

client=OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
)

response=client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[{"role": "user", "content": "Hello!"}],
    max_completion_tokens=150,
)

print('BEGIN LLM RESPONSE\n')
print(response.choices[0].message.content)
print('\nEND LLM RESPONSE')
