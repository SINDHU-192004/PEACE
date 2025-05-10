import requests
import os
import pandas as pd
from tqdm import tqdm

# Create datasets directory if it doesn't exist
os.makedirs('datasets', exist_ok=True)

# URL of the GoEmotions dataset on Hugging Face
url = "https://huggingface.co/datasets/mrm8488/goemotions/resolve/main/goemotions.csv"

# Path to save the dataset
file_path = "datasets/goemotions.csv"

print(f"Downloading GoEmotions dataset from {url}...")

# Download the file
response = requests.get(url, stream=True)
response.raise_for_status()  # Raise an exception for HTTP errors

# Get total file size
total_size = int(response.headers.get('content-length', 0))
block_size = 1024  # 1 Kibibyte

# Show a progress bar during download
progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)

with open(file_path, 'wb') as file:
    for data in response.iter_content(block_size):
        progress_bar.update(len(data))
        file.write(data)

progress_bar.close()

print(f"Dataset downloaded and saved to {file_path}")

# Load and preview the dataset
try:
    df = pd.read_csv(file_path)
    print("\nDataset Preview:")
    print(f"Number of rows: {df.shape[0]}")
    print(f"Number of columns: {df.shape[1]}")
    print("\nFirst 5 rows:")
    print(df.head())
    
    # List all emotions in the dataset
    emotion_columns = [col for col in df.columns if col not in ['text', 'id', 'author', 'subreddit', 'link_id', 'parent_id', 'created_utc', 'rater_id', 'example_very_unclear']]
    print(f"\nEmotion labels ({len(emotion_columns)}):")
    print(", ".join(emotion_columns))
    
except Exception as e:
    print(f"Error loading the dataset: {e}") 