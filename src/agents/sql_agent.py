# src/agents/sql_agent.py

from langchain.sql_database import SQLDatabase
from langchain.agents.agent_toolkits import SQLDatabaseToolkit, create_sql_agent

def run(query: str, llm) -> str:
    # Initialize your FDOT database connection.
    db = SQLDatabase.from_uri("sqlite:///fdot_database.db")
    # Create a toolkit from your database and llm
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    # Create an SQL agent using the toolkit (not the raw db)
    sql_agent = create_sql_agent(llm, toolkit, verbose=True)
    return sql_agent.run(query)
