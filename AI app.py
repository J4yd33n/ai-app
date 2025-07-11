import streamlit as st
from transformers import pipeline, Conversation

# Initialize the conversational model
@st.cache_resource
def load_model():
    return pipeline("conversational", model="facebook/blenderbot-400M-distill")

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
    
    # Create a conversation object
    conversation = Conversation(user_input)
    
    # Get bot response
    response = chatbot(conversation)
    
    # Extract the bot's response
    bot_response = response.generated_responses[-1]
    
    # Add bot response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
    
    # Rerun to update the chat display
    st.rerun()

# Clear chat history button
if st.button("Clear Chat History"):
    st.session_state.chat_history = []
    st.rerun()
