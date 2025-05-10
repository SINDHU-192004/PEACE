# MentalMend Chatbot with Emotion Detection

This chatbot is enhanced with emotion detection capabilities using the GoEmotions dataset from Google Research. It can identify 27 different emotions plus a neutral state in user messages, allowing for more empathetic and context-aware responses.

## Features

- Real-time emotion detection in user messages
- Emoji visualization of detected emotions
- Emotionally-aware AI responses
- Support for 28 different emotional states
- Streamlit-based web interface

## Setup Instructions

1. First, download the GoEmotions dataset:

```bash
python ../download_dataset.py
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Train the emotion detection model:

```bash
python train_emotion_model.py
```

4. Run the Streamlit app:

```bash
streamlit run app.py
```

## Emotion Categories

The chatbot can detect the following emotions:
- Admiration
- Amusement
- Anger
- Annoyance
- Approval
- Caring
- Confusion
- Curiosity
- Desire
- Disappointment
- Disapproval
- Disgust
- Embarrassment
- Excitement
- Fear
- Gratitude
- Grief
- Joy
- Love
- Nervousness
- Optimism
- Pride
- Realization
- Relief
- Remorse
- Sadness
- Surprise
- Neutral

## How It Works

1. When a user sends a message, the emotion detection model analyzes the text
2. The dominant emotion is identified and displayed with an emoji
3. The AI is given context about the user's emotional state
4. The AI generates a response that's appropriate for the detected emotion

## API Keys

To use the AI chatbot functionality, you'll need to provide an API key for Groq in a `.env` file:

```
GROQ_API_KEY=your_api_key_here
```

## Customization

You can modify the emotion responses in the `app.py` file to customize how the chatbot responds to different emotional states.

## About GoEmotions

GoEmotions is a dataset of 58k carefully curated Reddit comments annotated for 27 emotion categories and a Neutral category. For more information about the dataset, visit [Google Research's GoEmotions repository](https://github.com/google-research/google-research/tree/master/goemotions). 