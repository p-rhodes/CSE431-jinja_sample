#This is a test script so I can try out a free llm api since I no have the
#money for the claude api

from openai import OpenAI

if not os.getenv("GROQ_API_KEY"):
    raise SystemExit("No api key!")

client=OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY,
)

response=client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "Hello!"}],
)

print('BEGIN LLM RESPONSE\n')
print(response.choices[0].message.content)
print('\nEND LLM RESPONSE')
