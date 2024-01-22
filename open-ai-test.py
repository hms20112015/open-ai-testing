from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a poet."},
    {"role": "user", "content": "Compose a haiku about ice cream."}
  ]
)

print(completion.choices[0].message)