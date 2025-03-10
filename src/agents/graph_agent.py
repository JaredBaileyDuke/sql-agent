# src/agents/graph_agent.py

import matplotlib.pyplot as plt
import io
import base64

def run(query: str) -> str:
    """
    Generate a graph from input data.
    Expects the query to be a comma-separated list of numbers.
    Returns a base64 encoded image string.
    """
    try:
        # Convert comma-separated values into a list of floats.
        data = [float(x.strip()) for x in query.split(',')]
    except Exception as e:
        return f"Error parsing input data: {e}"
    
    plt.figure()
    plt.plot(data)
    plt.title("Generated Graph")
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()
    return f"data:image/png;base64,{image_base64}"
