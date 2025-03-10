# src/agents/master_agent.py

import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain.callbacks.base import BaseCallbackHandler

# Load environment variables from .env file
load_dotenv()

class ChainOfThoughtHandler(BaseCallbackHandler):
    """
    A custom callback handler to capture the chain-of-thought (CoT)
    and record which tools were used during execution.
    """
    def __init__(self):
        self.chain = []
        self.tools_used = set()

    def on_agent_action(self, action, **kwargs):
        self.chain.append(f"Using tool: {action.tool} with input: {action.tool_input}")
        self.tools_used.add(action.tool)

    def on_agent_finish(self, finish, **kwargs):
        if isinstance(finish.return_values, dict) and "output" in finish.return_values:
            self.chain.append(f"Final answer: {finish.return_values['output']}")
        else:
            self.chain.append(f"Final answer: {finish.return_values}")

class MasterAgent:
    def __init__(self, verbose: bool = False):
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("Please set the OPENAI_API_KEY environment variable in your .env file.")
        
        self.llm = OpenAI(api_key=openai_api_key, temperature=0, verbose=verbose)
        # Initialize flag to track if SQLAgent has been called
        self.sql_called = False
        
        # Import subordinate agents.
        from src.agents import search_tool
        # from src.agents import fdot_bot_agent  # FDOT Bot is commented out for now.
        # Uncomment SQLAgent and GraphAgent as needed.
        # from src.agents import sql_agent, graph_agent  # Uncomment if used.
        
        self.tools = [
            # Tool(
            #     name="InternetSearch",
            #     func=search_tool.run,
            #     description="Performs an internet search if the answer isn’t in the database."
            # ),
            # Tool(
            #     name="SQLAgent",
            #     func=self._run_sql_agent,
            #     description="Queries the FDOT SQL database for relevant information."
            # ),
            Tool(
                name="GraphAgent",
                func=self._run_graph_agent,
                description="Generates graphs based on provided numerical data. (Available after SQLAgent is used.)"
            ),
            Tool(
                name="PandasAgent",
                func=self._run_pandas_agent,
                description="Performs analysis on CSV data using a Pandas DataFrame."
            ),
            Tool(
                name="Text Agent",
                func=self.text_agent,
                description="A simple agent that echoes back the provided input."
            )
        ]
        
        # Allow all the tools we just defined.
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent="zero-shot-react-description",
            verbose=verbose,
            allowed_tools=["InternetSearch", "SQLAgent", "GraphAgent", "PandasAgent", "Text Agent"]
        )
    
    def _run_sql_agent(self, query: str) -> str:
        # Mark that SQLAgent has been run.
        self.sql_called = True
        from src.agents import sql_agent
        return sql_agent.run(query, self.llm)
        
    def _run_pandas_agent(self, query: str) -> str:
        from src.agents import pandas_agent
        return pandas_agent.run(query, self.llm)
    
    def _run_graph_agent(self, query: str) -> str:
        # Only allow GraphAgent if SQLAgent has been called.
        if not self.sql_called:
            return "Graph Agent unavailable. Please run SQL Agent first."
        from src.agents import graph_agent
        return graph_agent.run(query)
    
    def text_agent(self, input_text: str) -> str:
        return f"Text Agent processed: {input_text}"
    
    def run(self, prompt: str) -> str:
        # Attempt to open and read the DATABASE.md document for context.
        try:
            with open("./src/data/CSV.md", "r") as file:
                database_doc = file.read()
        except Exception as e:
            database_doc = ""
        
        # Prepend the database documentation to the user prompt.
        prompt_with_doc = (
            f"Please refer to the following database documentation to help determine "
            f"if the SQLAgent should be used:\n\n{database_doc}\n\nUser Query:\n{prompt}"
        )
        
        cot_handler = ChainOfThoughtHandler()
        result = self.agent.run(prompt_with_doc, callbacks=[cot_handler])
        
        formatted_lines = []
        for line in cot_handler.chain:
            if line.startswith("Using tool:"):
                if " with input:" in line:
                    parts = line.split(" with input:")
                    tool_name = parts[0].replace("Using tool:", "").strip()
                    input_value = parts[1].strip()
                    formatted_lines.append(f"- **Using tool:** {tool_name}")
                    formatted_lines.append(f"  **With input:** {input_value}")
                else:
                    tool_name = line.replace("Using tool:", "").strip()
                    formatted_lines.append(f"- **Using tool:** {tool_name}")
            elif line.startswith("Final answer:"):
                answer = line.replace("Final answer:", "").strip()
                formatted_lines.append(f"- **Final answer:** {answer}")
            else:
                formatted_lines.append(line)
        
        formatted_chain_text = "\n\n".join(formatted_lines)
        tools_list = ", ".join(cot_handler.tools_used)
        
        final_output = (
            f"{result}\n\n"
            f"## Chain-of-Thought\n\n"
            f"{formatted_chain_text}\n\n"
            f"**Tools Used:** {tools_list}"
        )
        return final_output

if __name__ == "__main__":
    master_agent = MasterAgent(verbose=True)
    test_prompt = "How many r's are in strawberry?"
    response = master_agent.run(test_prompt)
    print("Response:", response)
