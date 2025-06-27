# app/llm_router.py

from typing import Generator, List, Dict, Union
from groq import Groq
from app.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def chat_with_model(
    model: str, 
    messages: list, 
    temperature: float=0.7, 
    stream: bool=True
):
    """
    Send a chat completion request to Groq model via Groq’s official Python SDK.

    Args:
        model (str): Model name from config (e.g. llama-3.1-8b-instant)
        messages (list): Chat history in OpenAI format
        temperature (float): Creativity of response
        stream (bool): Whether to stram tokens (for UI)

    Returns:
    If stream=False: full response text
    If stream=True: generator yielding chunks
    """

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            stream=stream
        )

        if stream:
            for chunk in response:
                if chunk.choices[0].delta.content: # type: ignore
                    yield chunk.choices[0].delta.content # type: ignore

        else:
            return response.choices[0].message.content # type: ignore
        
    except Exception as e:
        print(f"[LLM Router] Error: {e}")
        return "⚠️ An error occurred while contacting the LLM."