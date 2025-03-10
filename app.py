import streamlit as st
import time

# Initialize session state for storing messages
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Watson Civil Database Chatbot")

def add_message(content, is_user=False):
    """Append a message to the session state."""
    st.session_state.messages.append({"content": content, "is_user": is_user})

# Display chat messages from session state with custom avatars
for msg in st.session_state.messages:
    avatar = "👷" if msg["is_user"] else "🧠"
    with st.chat_message("user" if msg["is_user"] else "assistant", avatar=avatar):
        st.markdown(msg["content"])

# Chat input field at the bottom
user_input = st.chat_input("Type your message...")

if user_input:
    # Append user message
    add_message(user_input, is_user=True)
    
    # Simulated bot reply
    reply_text = f"Bot says: {user_input}"
    
    # Stream the bot reply character-by-character
    with st.chat_message("assistant", avatar="🧠"):
        placeholder = st.empty()
        streamed_text = ""
        for char in reply_text:
            streamed_text += char
            placeholder.markdown(streamed_text)
            time.sleep(0.05)  # Adjust the speed as needed

    # Once streaming is complete, add the final reply to session state
    add_message(reply_text, is_user=False)
    
    # Rerun the app to update the chat display
    st.rerun()
