import os
import time
import requests

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
# Backward compatible timeout behavior:
# - If OLLAMA_READ_TIMEOUT_SECONDS is set, it is used.
# - Else, if legacy OLLAMA_TIMEOUT_SECONDS is set, that value is used as read timeout.
# - Else, default to a longer read timeout for larger prompts/models.
OLLAMA_CONNECT_TIMEOUT_SECONDS = int(os.getenv("OLLAMA_CONNECT_TIMEOUT_SECONDS", "10"))
OLLAMA_READ_TIMEOUT_SECONDS = int(
    os.getenv("OLLAMA_READ_TIMEOUT_SECONDS", os.getenv("OLLAMA_TIMEOUT_SECONDS", "900"))
)
OLLAMA_MAX_RETRIES = int(os.getenv("OLLAMA_MAX_RETRIES", "3"))


def _extract_error_details(response):
    try:
        payload = response.json()
        if isinstance(payload, dict):
            if payload.get("error"):
                return str(payload["error"])
            if payload.get("response"):
                return str(payload["response"])
    except ValueError:
        pass

    return response.text[:500] if response.text else "No error details returned by Ollama."


def call_llm(prompt):
    model = os.getenv("MODEL_NAME")
    if not model:
        raise ValueError("MODEL_NAME environment variable is not set")

    print(f"Using model: {model}")

    last_error = None
    for attempt in range(OLLAMA_MAX_RETRIES + 1):
        try:
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=(OLLAMA_CONNECT_TIMEOUT_SECONDS, OLLAMA_READ_TIMEOUT_SECONDS)
            )

            if response.status_code >= 500:
                details = _extract_error_details(response)
                raise requests.HTTPError(
                    f"Ollama server error ({response.status_code}): {details}",
                    response=response
                )

            response.raise_for_status()

            payload = response.json()
            result = payload.get("response", "").strip()
            if not result:
                raise ValueError("Ollama returned an empty response")

            return result
        except (requests.RequestException, ValueError) as exc:
            last_error = exc
            if attempt < OLLAMA_MAX_RETRIES:
                wait_seconds = attempt + 1
                print(
                    f"LLM request failed (attempt {attempt + 1}/{OLLAMA_MAX_RETRIES + 1}): {exc}. "
                    f"Retrying in {wait_seconds}s..."
                )
                time.sleep(wait_seconds)
                continue
            break

    raise RuntimeError(f"Failed to get LLM response from {OLLAMA_URL}: {last_error}") from last_error