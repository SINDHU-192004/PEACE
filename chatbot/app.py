import streamlit as st
import requests
from dotenv import load_dotenv
import os
import time
from emotion_detector import EmotionDetector

# Streamlit page setup - MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(page_title="MentalMend Chatbot", layout="centered", page_icon="🤖")

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# DEBUG: Check if the key is loaded
if GROQ_API_KEY:
    st.sidebar.success("✅ GROQ API Key loaded successfully!")
else:
    st.sidebar.error("❌ GROQ API Key not found. Check your .env file.")

# Initialize emotion detector
emotion_detector = EmotionDetector(
    model_path='emotion_model.pkl',
    vectorizer_path='vectorizer.pkl'
)

# Train model if it doesn't exist
if (not os.path.exists(emotion_detector.model_path) or 
    not os.path.exists(emotion_detector.vectorizer_path)):
    st.info("Training emotion detection model. This may take a few minutes...")
    emotion_detector.train('../datasets/goemotions.csv')
    st.success("Model training complete!")
else:
    # Load the model
    emotion_detector.load_model()

# Emotion emoji mapping
emotion_emojis = {
    'admiration': '😍',
    'amusement': '😂',
    'anger': '😡',
    'annoyance': '😒',
    'approval': '👍',
    'caring': '🤗',
    'confusion': '😕',
    'curiosity': '🤔',
    'desire': '😍',
    'disappointment': '😞',
    'disapproval': '👎',
    'disgust': '🤢',
    'embarrassment': '😳',
    'excitement': '🤩',
    'fear': '😨',
    'gratitude': '🙏',
    'grief': '😢',
    'joy': '😄',
    'love': '❤️',
    'nervousness': '😬',
    'optimism': '🤞',
    'pride': '🦁',
    'realization': '💡',
    'relief': '😌',
    'remorse': '😔',
    'sadness': '😭',
    'surprise': '😮',
    'neutral': '😐'
}

# Emotion-based response suggestions
emotion_responses = {
    'sadness': [
        "I understand you're feeling down. Remember that difficult times are temporary.",
        "It sounds like you're going through a hard time. Is there anything specific that's bothering you?",
        "I'm sorry to hear you're feeling sad. Would talking about it help?"
    ],
    'anger': [
        "I can sense you're feeling frustrated. Taking a few deep breaths might help.",
        "It seems like you're upset. Would you like to talk about what's bothering you?",
        "I understand you're angry. Sometimes expressing these feelings can help process them."
    ],
    'fear': [
        "It's okay to feel scared. Can you tell me more about what's making you fearful?",
        "I understand that feeling afraid can be overwhelming. You're not alone in this.",
        "Fear is a natural response. Would it help to break down what's causing this anxiety?"
    ],
    'joy': [
        "I'm happy to see you're in good spirits! What's bringing you joy today?",
        "That sounds wonderful! It's great to celebrate these positive moments.",
        "I'm glad you're feeling good! Your positive energy is contagious."
    ],
    'love': [
        "That's beautiful to hear. Love is such a powerful emotion.",
        "I'm happy you're experiencing such positive feelings.",
        "That sounds really meaningful. Would you like to share more?"
    ]
}

st.markdown(
    "<h1 style='text-align: center; color: #3b82f6;'>🤖 MentalMend</h1>", 
    unsafe_allow_html=True
)
st.markdown("<p style='text-align: center;'>I'm here for you &lt;3</p>", unsafe_allow_html=True)

# Store conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages with emotions
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if "emotion" in msg and msg["emotion"] != "neutral":
            emoji = emotion_emojis.get(msg["emotion"], "")
            st.markdown(f"{msg['content']} {emoji}")
        else:
            st.markdown(msg["content"])

# Get user input
user_input = st.chat_input("How are you feeling?")
if user_input:
    # Detect emotion
    emotion = emotion_detector.get_dominant_emotion(user_input)
    emoji = emotion_emojis.get(emotion, "")
    
    # Show user message with emotion
    st.chat_message("user").markdown(f"{user_input} {emoji}")
    st.session_state.messages.append({
        "role": "user", 
        "content": user_input,
        "emotion": emotion
    })
    
    # Add emotion context to the AI input
    ai_context = ""
    if emotion in emotion_responses:
        ai_context = f"[Note: The user seems to be expressing {emotion}. Consider a response like: {emotion_responses[emotion][0]}] "

    # Prepare API request to Groq
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    # Create messages for API with emotion context
    api_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
    
    # Add system message with emotion context for the latest message
    api_messages.insert(0, {
        "role": "system", 
        "content": f"You are a helpful and empathetic mental health assistant. {ai_context}"
    })

    payload = {
        "model": "llama3-8b-8192",
        "messages": api_messages,
        "temperature": 0.7,
        "max_tokens": 1024
    }

    try:
        with st.spinner("Thinking..."):
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            reply = response.json()["choices"][0]["message"]["content"]

        # Show bot reply
        st.chat_message("assistant").markdown(reply)
        st.session_state.messages.append({
            "role": "assistant", 
            "content": reply,
            "emotion": "neutral"  # AI doesn't have emotions
        })
    except Exception as e:
        st.error(f"Something went wrong: {e}")
        
# Add sidebar with emotion information
with st.sidebar:
    st.title("About GoEmotions")
    st.write("""
    This chatbot is powered by the GoEmotions dataset from Google Research, 
    which recognizes 27 different emotions plus neutral.
    
    The model analyzes your messages to understand your emotional state and
    provides more empathetic responses.
    """)
    
    st.subheader("Detectable Emotions")
    emotion_cols = st.columns(2)
    
    for i, (emotion, emoji) in enumerate(emotion_emojis.items()):
        col_idx = i % 2
        emotion_cols[col_idx].write(f"{emoji} {emotion.capitalize()}")
    
    st.subheader("How It Works")
    st.write("""
    1. You type a message
    2. The model detects your emotion
    3. The AI gets context about your emotion
    4. The response is tailored to your emotional state
    """)