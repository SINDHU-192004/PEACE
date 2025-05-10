import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import pickle
import os
import time

class EmotionDetector:
    def __init__(self, model_path='emotion_model.pkl', vectorizer_path='vectorizer.pkl'):
        """Initialize the emotion detector."""
        self.model_path = model_path
        self.vectorizer_path = vectorizer_path
        self.model = None
        self.vectorizer = None
        self.emotions = ['admiration', 'amusement', 'anger', 'annoyance', 'approval', 'caring', 
                         'confusion', 'curiosity', 'desire', 'disappointment', 'disapproval', 
                         'disgust', 'embarrassment', 'excitement', 'fear', 'gratitude', 'grief', 
                         'joy', 'love', 'nervousness', 'optimism', 'pride', 'realization', 
                         'relief', 'remorse', 'sadness', 'surprise', 'neutral']
    
    def load_dataset(self, csv_path):
        """Load the GoEmotions dataset from CSV."""
        print(f"Loading dataset from {csv_path}")
        df = pd.read_csv(csv_path)
        
        # Select only the first annotation for each text to simplify the dataset
        df = df.drop_duplicates(subset=['text'])
        
        # Extract features (text) and labels (emotions)
        X = df['text']
        y = df[self.emotions]
        
        return X, y
    
    def train(self, csv_path, test_size=0.2):
        """Train the emotion detection model."""
        start_time = time.time()
        print("Starting training...")
        
        # Load the dataset
        X, y = self.load_dataset(csv_path)
        
        # Split the dataset
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
        
        # Store training stats
        self.train_examples = len(X_train)
        self.test_examples = len(X_test)
        
        print(f"Training on {len(X_train)} examples, testing on {len(X_test)} examples")
        
        # Create a TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(max_features=10000)
        
        # Create a multi-output classifier with LinearSVC
        svc = LinearSVC(random_state=42, max_iter=1000)
        self.model = MultiOutputClassifier(svc)
        
        # Train the model
        print("Vectorizing text...")
        X_train_vec = self.vectorizer.fit_transform(X_train)
        
        print("Training the model (this may take a while)...")
        self.model.fit(X_train_vec, y_train)
        
        # Evaluate the model
        X_test_vec = self.vectorizer.transform(X_test)
        self.accuracy = self.model.score(X_test_vec, y_test)
        print(f"Model accuracy: {self.accuracy:.4f}")
        
        # Save the model and vectorizer
        print("Saving model and vectorizer...")
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)
        
        with open(self.vectorizer_path, 'wb') as f:
            pickle.dump(self.vectorizer, f)
        
        end_time = time.time()
        self.training_time = end_time - start_time
        print(f"Training completed in {self.training_time:.2f} seconds")
    
    def load_model(self):
        """Load the pre-trained model and vectorizer."""
        try:
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            
            with open(self.vectorizer_path, 'rb') as f:
                self.vectorizer = pickle.load(f)
            
            print("Model and vectorizer loaded successfully")
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def predict(self, text):
        """Predict emotions from text."""
        if self.model is None or self.vectorizer is None:
            if not self.load_model():
                return {"error": "Model not loaded"}
        
        # Vectorize the text
        text_vec = self.vectorizer.transform([text])
        
        # Predict emotions
        predictions = self.model.predict(text_vec)[0]
        
        # Convert predictions to a dictionary
        emotion_dict = {}
        for emotion, value in zip(self.emotions, predictions):
            if value > 0:
                emotion_dict[emotion] = float(value)
        
        # If no emotions were detected, return neutral
        if not emotion_dict:
            emotion_dict["neutral"] = 1.0
        
        return emotion_dict
    
    def get_dominant_emotion(self, text):
        """Get the dominant emotion from the text."""
        emotions = self.predict(text)
        if "error" in emotions:
            return "neutral"
        
        # Return the emotion with the highest score
        return max(emotions.items(), key=lambda x: x[1])[0]


# Simple test for the detector
if __name__ == "__main__":
    detector = EmotionDetector()
    
    # Check if model exists, if not train it
    if (not os.path.exists(detector.model_path) or 
        not os.path.exists(detector.vectorizer_path)):
        print("Model not found. Training a new model...")
        detector.train('../datasets/goemotions.csv')
    
    # Test the detector
    texts = [
        "I'm so happy today!",
        "This makes me really angry.",
        "I'm feeling sad and lonely.",
        "That's hilarious!",
        "I'm confused about what happened.",
    ]
    
    for text in texts:
        emotion = detector.get_dominant_emotion(text)
        print(f"Text: '{text}' → Dominant emotion: {emotion}") 