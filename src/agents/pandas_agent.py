import pandas as pd
from langchain_experimental.agents import create_pandas_dataframe_agent

def run(query: str, llm) -> str:
    # Load CSV data into a pandas DataFrame.
    try:
        df = pd.read_csv("src/data/DedupeContract_202502192343.csv")
    except Exception as e:
        return f"Error reading CSV file: {str(e)}"
    
    # Read CSV documentation.
    try:
        with open("src/data/CSV.md", "r") as file:
            csv_doc = file.read()
    except Exception as e:
        csv_doc = ""
    
    # Create a pandas agent, enabling dangerous code execution if needed.
    agent = create_pandas_dataframe_agent(
        llm,
        df,
        verbose=True,
        allow_dangerous_code=True
    )
    
    # Prepend the CSV documentation to the user query.
    full_query = (
        f"Please refer to the following CSV documentation before answering:\n\n"
        f"{csv_doc}\n\nUser Query:\n{query}"
    )
    
    # Run the agent with the full query.
    return agent.run(full_query)
