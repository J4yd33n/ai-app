import streamlit as st
from transformers import pipeline

# Initialize the conversational model
@st.cache_resource
def load_model():
    return pipeline("text-generation", model="facebook/blenderbot-400M-distill")

# Load the model
chatbot = load_model()

# Streamlit app layout
st.title("AI Chatbot")
st.write("Chat with the AI! Type your message below, and the bot will respond.")

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # Prepare conversation history for the model (limited to last 5 turns for memory efficiency)
    history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.chat_history[-10:]])
    
    # Get bot response
    with st.spinner("Bot is thinking..."):
        response = chatbot(user_input, max_length=100, num_return_sequences=1, do_sample=True, truncation=True)[0]['generated_text']
        # Clean up response (remove user input prefix if present)
        response = response.replace(user_input, "").strip()
    
    # Add bot response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    # Limit history to prevent memory issues
    if len(st.session_state.chat_history) > 20:  # Keep last 10 turns (20 messages)
        st.session_state.chat_history = st.session_state.chat_history[-20:]
    
    # Rerun to update the chat display
    st.rerun()

# Clear chat history button
if st.button("Clear Chat History"):
    st.session_state.chat_history = []
    st.rerun()
