#!/usr/bin/env python
import os
import subprocess
import sys
import time

def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f" {text} ".center(60, "="))
    print("=" * 60 + "\n")

def run_command(command, description=None):
    """Run a command and print its output."""
    if description:
        print(f"\n> {description}...")
    
    try:
        process = subprocess.Popen(
            command, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            universal_newlines=True
        )
        
        for line in process.stdout:
            print(line.strip())
        
        process.wait()
        return process.returncode == 0
    except Exception as e:
        print(f"Error executing command: {e}")
        return False

def main():
    print_header("PEACE Mental Health Platform - Setup")
    print("This script will set up the PEACE platform with the GoEmotions dataset integration.")
    
    # Check Python version
    python_version = sys.version_info
    print(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 6):
        print("ERROR: Python 3.6 or higher is required.")
        return
    
    # Create directories
    os.makedirs("datasets", exist_ok=True)
    
    # 1. Download the dataset if not exists
    print_header("Step 1: Downloading GoEmotions Dataset")
    dataset_path = os.path.join("datasets", "goemotions.csv")
    if os.path.exists(dataset_path):
        print(f"Dataset already exists at {dataset_path}. Skipping download.")
    else:
        print(f"Dataset not found at {dataset_path}.")
        success = run_command("python download_dataset.py", "Downloading dataset")
        if not success:
            print("Failed to download the dataset. Please check your internet connection.")
            return
    
    # 2. Install dependencies
    print_header("Step 2: Installing Dependencies")
    requirements_path = os.path.join("chatbot", "requirements.txt")
    if not os.path.exists(requirements_path):
        print(f"Requirements file not found at {requirements_path}.")
        return
        
    success = run_command(f"pip install -r {requirements_path}", "Installing required packages")
    if not success:
        print("Failed to install dependencies. Please check the error messages above.")
        return
    
    # 3. Train the emotion model
    print_header("Step 3: Training Emotion Detection Model")
    model_path = os.path.join("chatbot", "emotion_model.pkl")
    vectorizer_path = os.path.join("chatbot", "vectorizer.pkl")
    
    if os.path.exists(model_path) and os.path.exists(vectorizer_path):
        print(f"Emotion model already exists at {model_path}. Skipping training.")
        retrain = input("Would you like to retrain the model anyway? (y/n): ")
        if retrain.lower() == 'y':
            success = run_command("python chatbot/train_emotion_model.py", "Training emotion model")
            if not success:
                print("Failed to train the emotion model. Please check the error messages above.")
                return
    else:
        print(f"Emotion model not found. Training now...")
        success = run_command("python chatbot/train_emotion_model.py", "Training emotion model")
        if not success:
            print("Failed to train the emotion model. Please check the error messages above.")
            return
    
    # 4. Complete
    print_header("Setup Complete!")
    print("""
The PEACE platform with GoEmotions integration has been successfully set up!

To start the chatbot, run:
    cd chatbot
    streamlit run app.py

To view the web interface, open index.html in your browser or use a local server:
    python -m http.server

Thank you for using PEACE!
    """)

if __name__ == "__main__":
    main() 