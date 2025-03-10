# src/agents/search_tool.py

import os
from dotenv import load_dotenv
from langchain.utilities import SerpAPIWrapper

# Load environment variables from .env file
load_dotenv()

# Retrieve the SERPAPI_API_KEY from the environment
serpapi_api_key = os.getenv("SERPAPI_API_KEY")
if not serpapi_api_key:
    raise ValueError("Please set the SERPAPI_API_KEY environment variable in your .env file.")

# Initialize the SerpAPIWrapper with the proper parameter name
serpapi = SerpAPIWrapper(serpapi_api_key=serpapi_api_key)

def run(query: str) -> str:
    """Perform an internet search for the given query."""
    return serpapi.run(query)
