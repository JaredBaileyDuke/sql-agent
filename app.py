import streamlit as st
import time
from src.agents.master_agent import MasterAgent

# Initialize session state variables if they don't exist.
if "messages" not in st.session_state:
    st.session_state.messages = []
if "master_agent" not in st.session_state:
    st.session_state.master_agent = MasterAgent(verbose=True)
if "pending_input" not in st.session_state:
    st.session_state.pending_input = None

st.title("Music Sales Database Chatbot")

def add_message(content, is_user=False):
    """Append a message to the session state."""
    st.session_state.messages.append({"content": content, "is_user": is_user})

# Display chat messages with custom avatars.
for msg in st.session_state.messages:
    avatar = "👷" if msg["is_user"] else "🧠"
    with st.chat_message("user" if msg["is_user"] else "assistant", avatar=avatar):
        st.markdown(msg["content"])

# If there's a pending user input waiting to be processed, process it now.
if st.session_state.pending_input:
    user_input = st.session_state.pending_input
    # Call the master agent to process the user input (this is a blocking call).
    response_text = st.session_state.master_agent.run(user_input)
    
    # Optionally, you can stream the response character-by-character:
    with st.chat_message("assistant", avatar="🧠"):
        placeholder = st.empty()
        streamed_text = ""
        for char in response_text:
            streamed_text += char
            placeholder.markdown(streamed_text)
            time.sleep(0.01)  # Adjust the speed as desired

    # Save the complete reply in session state.
    add_message(response_text, is_user=False)
    # Clear the pending input so it doesn't get reprocessed.
    st.session_state.pending_input = None
    st.rerun()

# Chat input field at the bottom.
user_input = st.chat_input("Type your message...")

if user_input:
    # Immediately add the user message.
    add_message(user_input, is_user=True)
    # Save the user input as pending to be processed on the next run.
    st.session_state.pending_input = user_input
    st.rerun()
