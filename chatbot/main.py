import requests
from emotion_detector import EmotionDetector

# Your OpenRouter API key
API_KEY = "c86f97014f5a60d01e85903a5f2a7a7989b1628f"
BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

# Initialize and load emotion detection model
detector = EmotionDetector()
if not detector.load_model():
    print("Training model as no pre-trained model was found...")
    detector.train('../datasets/goemotions.csv')

# Function to chat with GPT via OpenRouter API
def chat_with_gpt(user_input):
    emotion = detector.get_dominant_emotion(user_input)
    prompt = f"The user is feeling {emotion}. Respond with empathy and suggest helpful mental health tips.\nUser: {user_input}"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",  # You can replace with other models like "mistralai/mixtral-8x7b"
        "messages": [
            {"role": "system", "content": "You are a kind and empathetic mental health assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(BASE_URL, headers=headers, json=data)
        if response.status_code == 200:
            reply = response.json()['choices'][0]['message']['content'].strip()
            return reply, emotion
        else:
            print(f"API Error {response.status_code}: {response.text}")
            return "Sorry, something went wrong while processing your request.", emotion
    except Exception as e:
        print(f"Exception occurred: {e}")
        return "Sorry, I couldn't process your request due to a system error.", emotion

# Example CLI loop (optional, remove if using a web UI)
if __name__ == "__main__":
    print("Mental Health Assistant (Type 'exit' to quit)\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        response, emotion = chat_with_gpt(user_input)
        print(f"Assistant ({emotion}): {response}\n")
