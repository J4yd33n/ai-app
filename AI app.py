import streamlit as st
from transformers import pipeline

# Initialize the sentiment analysis pipeline
@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis")

# Load the model
classifier = load_model()

# Streamlit app layout
st.title("AI Sentiment Analysis App")
st.write("Enter text to analyze its sentiment (positive or negative).")

# Text input
user_input = st.text_area("Enter your text here:", height=150)

# Analyze button
if st.button("Analyze Sentiment"):
    if user_input:
        # Perform sentiment analysis
        result = classifier(user_input)[0]
        label = result['label']
        score = result['score']
        
        # Display results
        st.write(f"**Sentiment:** {label}")
        st.write(f"**Confidence Score:** {score:.2%}")
    else:
        st.warning("Please enter some text to analyze.")

# Add some example texts
st.subheader("Try these examples:")
if st.button("Example 1: Positive"):
    st.text_area("Example text", value="I absolutely love this product! It's amazing!", key="ex1")
if st.button("Example 2: Negative"):
    st.text_area("Example text", value="This was a terrible experience, very disappointing.", key="ex2")
