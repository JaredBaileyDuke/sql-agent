# src/agents/master_agent.py

import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI

# Load environment variables from .env file
load_dotenv()

class MasterAgent:
    def __init__(self, verbose: bool = False):
        # Retrieve OpenAI API key from the environment variable
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("Please set the OPENAI_API_KEY environment variable in your .env file.")

        # Initialize the base language model with your API key.
        self.llm = OpenAI(api_key=openai_api_key, temperature=0, verbose=verbose)
        
        # Define tools representing subordinate agents.
        # You can add more tools here to handle different tasks.
        self.tools = [
            Tool(
                name="ExampleAgent",
                func=self.example_agent,
                description="A simple agent that echoes back the provided input."
            ),
            # You can add additional tools, for example:
            # Tool(
            #     name="MathAgent",
            #     func=lambda expression: str(eval(expression)),  # Use with caution!
            #     description="Evaluates simple math expressions."
            # ),
        ]
        
        # Create the master agent using a zero-shot-react description approach.
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent="zero-shot-react-description",
            verbose=verbose
        )

    def example_agent(self, input_text: str) -> str:
        """
        A placeholder tool function that processes input text.
        Replace or extend this method with your desired functionality.
        """
        return f"ExampleAgent processed: {input_text}"

    def run(self, prompt: str) -> str:
        """
        Run the master agent with the provided prompt.
        This will use the agent's internal reasoning to select and call the appropriate tool.
        """
        return self.agent.run(prompt)

# For testing the module independently.
if __name__ == "__main__":
    master_agent = MasterAgent(verbose=True)
    test_prompt = "Test: call ExampleAgent with this input."
    response = master_agent.run(test_prompt)
    print("Response:", response)
