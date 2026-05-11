import os
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


def call_llm(prompt):

    model = os.getenv("MODEL_NAME")

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )

    response.raise_for_status()

    return response.json()["response"]