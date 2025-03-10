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
        # Log the tool usage with input.
        self.chain.append(f"Using tool: {action.tool} with input: {action.tool_input}")
        self.tools_used.add(action.tool)

    def on_agent_finish(self, finish, **kwargs):
        if isinstance(finish.return_values, dict) and "output" in finish.return_values:
            self.chain.append(f"Final answer: {finish.return_values['output']}")
        else:
            self.chain.append(f"Final answer: {finish.return_values}")

class MasterAgent:
    def __init__(self, verbose: bool = False):
        # Retrieve OpenAI API key from the environment.
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("Please set the OPENAI_API_KEY environment variable in your .env file.")
        
        # Initialize the base language model.
        self.llm = OpenAI(api_key=openai_api_key, temperature=0, verbose=verbose)
        
        # Import subordinate agents.
        from src.agents import search_tool
        # from src.agents import sql_agent, graph_agent  # Commented out for now
        
        # Define the list of tools the master agent can use.
        self.tools = [
            Tool(
                name="InternetSearch",
                func=search_tool.run,  # Assumes search_tool.py exports a run(query: str) -> str function.
                description="Performs an internet search if the answer isn’t in the database."
            ),
            Tool(
                name="Text Agent",
                func=self.text_agent,
                description="A simple agent that echoes back the provided input."
            )
        ]
        
        # Initialize the master agent using a zero-shot-react description approach.
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent="zero-shot-react-description",
            verbose=verbose
        )

    def text_agent(self, input_text: str) -> str:
        """A simple tool that echoes back the provided input."""
        return f"Text Agent processed: {input_text}"

    def run(self, prompt: str) -> str:
        """
        Run the master agent with the provided prompt.
        Returns the final answer along with a formatted chain-of-thought (CoT)
        and a list of all tools used.
        """
        # Capture intermediate steps.
        cot_handler = ChainOfThoughtHandler()
        result = self.agent.run(prompt, callbacks=[cot_handler])
        
        # Format each line of the chain-of-thought.
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

# For testing the module independently.
if __name__ == "__main__":
    master_agent = MasterAgent(verbose=True)
    test_prompt = "Test"
    response = master_agent.run(test_prompt)
    print("Response:", response)
