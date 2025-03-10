# src/agents/fdot_bot_agent.py

import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def run(prompt: str) -> str:
    messages = [
        {"role": "system", "content": "You are FDOT Bot, an expert OpenAI agent specialized in FDOT-related queries for civil engineering construction."},
        {"role": "user", "content": prompt}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-4",      # or your preferred model
        messages=messages,
        temperature=0.0,    # adjust as needed
    )
    
    return response.choices[0].message.content.strip()
