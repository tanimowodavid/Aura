from openai import OpenAI

client = OpenAI()


def call_llm(messages, model="gpt-4.1-mini"):
    """
    Thin wrapper around OpenAI chat completions.
    """
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.4,
    )
    return response.choices[0].message.content
