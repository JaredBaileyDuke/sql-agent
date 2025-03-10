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
        
        # Import subordinate agents.
        from src.agents import search_tool
        # from src.agents import fdot_bot_agent  # FDOT Bot is commented out for now.
        # from src.agents import sql_agent, graph_agent  # SQL and Graph agents are commented out for now.
        
        self.tools = [
            # Tool(
            #     name="FDOT Bot",
            #     func=fdot_bot_agent.run,
            #     description="The OpenAI FDOT Bot for FDOT-specific queries."
            # ),
            Tool(
                name="InternetSearch",
                func=search_tool.run,
                description="Performs an internet search if the answer isn’t in the database."
            ),
            # Tool(
            #     name="SQLAgent",
            #     func=self._run_sql_agent,
            #     description="Queries the FDOT SQL database for relevant information."
            # ),
            # Tool(
            #     name="GraphAgent",
            #     func=graph_agent.run,
            #     description="Generates graphs based on provided numerical data."
            # ),
            Tool(
                name="Text Agent",
                func=self.text_agent,
                description="A simple agent that echoes back the provided input."
            )
        ]
        
        # You can restrict the allowed tools if desired:
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent="zero-shot-react-description",
            verbose=verbose,
            allowed_tools=["InternetSearch", "Text Agent"]
        )

    # Helper function for SQLAgent, commented out for now.
    # def _run_sql_agent(self, query: str) -> str:
    #     from src.agents import sql_agent
    #     return sql_agent.run(query, self.llm)

    def text_agent(self, input_text: str) -> str:
        return f"Text Agent processed: {input_text}"

    def run(self, prompt: str) -> str:
        cot_handler = ChainOfThoughtHandler()
        result = self.agent.run(prompt, callbacks=[cot_handler])
        
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
