import streamlit as st
from st_chat_message import message

# Initialize session state to store messages
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Watson Civil Database Chatbot")

def add_message(content, is_user=False):
    st.session_state.messages.append({"content": content, "is_user": is_user})

# Render the chat messages using st-chat-message with unique keys
for i, msg in enumerate(st.session_state.messages):
    message(msg["content"], is_user=msg["is_user"], key=f"msg_{i}")

# Sidebar input area
with st.sidebar:
    st.header("User Input")
    user_input = st.text_input("Type your message:", key="user_input")
    if st.button("Send", key="send_btn"):
        if user_input:
            # Append the user's message
            add_message(user_input, is_user=True)
            # Bot response (for now, echoing back the user's message)
            bot_reply = f"Bot says: {user_input}"
            add_message(bot_reply, is_user=False)
            st.rerun()  # Corrected function to rerun the script
