# src/agents/sql_agent.py

from langchain.sql_database import SQLDatabase
from langchain.agents.agent_toolkits import SQLDatabaseToolkit, create_sql_agent

def run(query: str, llm) -> str:
    try:
        # Initialize your FDOT database connection.
        db = SQLDatabase.from_uri("sqlite:///CombinedContracts.db")
    except Exception as e:
        return f"Error: Unable to connect to the database. Details: {str(e)}"
    
    # Output the table names
    table_names = db.get_table_names()
    print(f"Connected to database. Available tables: {table_names}")
    
    # Check if the table 'DedupeContracts' exists
    if 'DedupeContracts' not in table_names:
        return "Error: Table 'DedupeContracts' does not exist in the database."
    
    # Create a toolkit from your database and llm
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    # Create an SQL agent using the toolkit (not the raw db)
    sql_agent = create_sql_agent(llm, toolkit, verbose=True)
    
    # Open and read the DATABASE.md file for context
    with open("./src/data/DATABASE.md", "r") as file:
        database_doc = file.read()
        
    # Prepend the DATABASE.md content to the user query
    full_query = f"Please refer to the following database documentation before answering:\n\n{database_doc}\n\nUser Query: {query}"
    return sql_agent.run(full_query)
