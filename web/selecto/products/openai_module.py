import openai
import config

openai.api_key = config.OPENAI_API_KEY


def define(text):
    response = openai.Completion.create(
        model="text-curie-001",
        prompt="Define: " + text,
        temperature=0.6
    )
    definition = response.choices[0].text
    return response, definition


def summarize(text):
    response = openai.Completion.create(
        model="text-curie-001",
        max_tokens=1024,
        prompt="Summarize: " + text,
        temperature=0.6
    )
    summary = response.choices[0].text
    return response, summary
