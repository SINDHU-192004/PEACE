import os
from emotion_detector import EmotionDetector

print("Training Emotion Detection Model for MentalMend")
print("=" * 50)

# Check if the dataset exists
dataset_path = '../datasets/goemotions.csv'
absolute_path = os.path.abspath(dataset_path)
if not os.path.exists(dataset_path):
    # Try alternate path
    dataset_path = 'datasets/goemotions.csv'
    absolute_path = os.path.abspath(dataset_path)
    if not os.path.exists(dataset_path):
        print(f"Dataset not found at either '../datasets/goemotions.csv' or 'datasets/goemotions.csv'")
        print("Please run download_dataset.py first to download the GoEmotions dataset.")
        exit(1)

print(f"Found dataset at {dataset_path} (absolute: {absolute_path})")

# Initialize the emotion detector
model_path = 'emotion_model.pkl'
vectorizer_path = 'vectorizer.pkl'
detector = EmotionDetector(model_path=model_path, vectorizer_path=vectorizer_path)

# Check if model already exists
if os.path.exists(model_path) and os.path.exists(vectorizer_path):
    print(f"Model files already exist at {model_path} and {vectorizer_path}")
    overwrite = input("Do you want to overwrite them? (y/n): ")
    if overwrite.lower() != 'y':
        print("Training cancelled.")
        exit(0)

# Train the model
print("\nStarting model training...\n")
detector.train(dataset_path)

# Test the model
print("\nTesting the model with sample sentences:\n")
test_sentences = [
    "I'm feeling really happy today!",
    "This is making me so angry",
    "I'm sad and feeling lonely",
    "That's so funny, I can't stop laughing",
    "I'm really confused about what just happened",
    "I'm nervous about the presentation tomorrow",
    "I'm grateful for your help",
    "I'm so excited for the weekend!",
    "I love spending time with my family",
    "I'm really afraid of what might happen"
]

print("-" * 50)
print("Sentence".ljust(40), "Detected Emotion")
print("-" * 50)

for sentence in test_sentences:
    emotion = detector.get_dominant_emotion(sentence)
    print(f"{sentence[:37] + '...' if len(sentence) > 37 else sentence.ljust(40)} {emotion}")

print("-" * 50)
print("\nModel training complete!")
print(f"Model saved to {model_path}")
print(f"Vectorizer saved to {vectorizer_path}")
print("\nYou can now run the chatbot app with: streamlit run app.py")

print("\nTraining statistics:")
print(f"Dataset used: {dataset_path}")
if hasattr(detector, 'train_examples') and hasattr(detector, 'test_examples'):
    print(f"Training on {detector.train_examples} examples, testing on {detector.test_examples} examples")
print(f"Vectorizing text...")
print(f"Training the model (this may take a while)...")
if hasattr(detector, 'accuracy'):
    print(f"Model accuracy: {detector.accuracy}")

print("\nSaving model and vectorizer...")
if hasattr(detector, 'training_time'):
    print(f"Training completed in {detector.training_time:.2f} seconds")

print("Streamlit app running on http://localhost:8501") 