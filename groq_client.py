from groq import Groq
from config import GROQ_API_KEY, MODEL

client = Groq(api_key=GROQ_API_KEY)

def call_llm(messages):
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.2,
        max_tokens=800
    )
    return response.choices[0].message.content


def stream_llm(messages):
    stream = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        stream=True,
        temperature=0.2
    )

    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta