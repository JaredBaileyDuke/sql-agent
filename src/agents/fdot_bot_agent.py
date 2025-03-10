# src/agents/fdot_bot_agent.py

import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set your API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def run(prompt: str) -> str:
    """
    Calls the OpenAI API directly as FDOT Bot.
    The system prompt instructs the model to behave as FDOT Bot.
    """
    messages = [
        {"role": "system", "content": "You are FDOT Bot, an expert OpenAI agent specialized in FDOT-related queries for civil engineering construction. Answer clearly and concisely."},
        {"role": "user", "content": prompt}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-4",      # Or use a different model if preferred.
        messages=messages,
        temperature=0.0,    # Adjust as needed.
    )
    
    return response.choices[0].message.content.strip()
