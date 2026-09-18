import os
from dotenv import load_dotenv
from groq import Groq, GroqError

from app.core.exceptions import GenerationError

# Ensure environment variables are loaded
load_dotenv()


def generate(system_prompt: str, user_prompt: str) -> str:
    provider = os.getenv("LLM_PROVIDER", "groq")
    if provider != "groq":
        raise GenerationError(f"Unsupported LLM_PROVIDER: {provider}")

    try:
        return _generate_groq(system_prompt, user_prompt)
    except GroqError as e:
        raise GenerationError(f"LLM generation failed via Groq: {e}") from e
    except Exception as e:
        raise GenerationError(f"Unexpected error during generation: {e}") from e


def _generate_groq(system_prompt: str, user_prompt: str) -> str:
    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        raise GenerationError("LLM_API_KEY is not set in your .env file.")

    client = Groq(api_key=api_key)
    model_name = os.getenv("LLM_MODEL", "openai/gpt-oss-120b").strip()

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.1,
    )
    return response.choices[0].message.content