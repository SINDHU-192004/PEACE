#  PEACE – Healthcare Meets Mental Wellness

**Track:** Healthcare for All  
**Team:** CODE wAt

PEACE is a virtual mental healthcare platform designed to ensure accessibility, affordability, and sustainability. It brings together real-time chatbot support, AI-powered wellness tools, and secure communication channels to bridge the gap between traditional mental healthcare systems and modern digital solutions.

---

##  Features

- **Virtual Chatbot** – Real-time support using **LLaMA 3.1**, available 24/7 for immediate mental health guidance.
- **Voice Interaction** – Chatbot voice interaction powered by **p5.js** for a more natural and comforting experience.
- **Emotion Detection** – **NEW!** Built with the **GoEmotions** dataset to analyze your emotional state and provide tailored responses.
- **Personalized Insights** – AI-powered analytics that track usage patterns and provide smart, data-driven wellness suggestions.
- **Progress Statistics Dashboard** – Visual stats to help users monitor their mental health journey and growth over time.
- **Community Support** – A safe space for users to connect, share, and support each other through moderated forums and discussions.
- **Affordable Consultations** – On-demand sessions with licensed professionals at low cost, making therapy more accessible.
- **Stress-relief Games** – Relaxing and therapeutic games developed with **Phaser.js** to boost focus and resilience.
- **Personalized Nutrition Plans** – Smart food suggestions curated to improve mood and mental well-being.
- **Guided Exercises** – Daily wellness activities and calming routines to promote mental clarity and physical vitality.
- **End-to-End Encryption** – Robust security ensuring all user data and conversations are kept private and protected.
  
---

## 🛠️ Tech Stack

| Area             | Tools Used                             |
|------------------|----------------------------------------|
| Frontend         | HTML, Tailwind CSS, JavaScript         |
| Backend          | Node.js                                |
| Chatbot          | Python, RiveScript, p5.speech          |
| Emotion Analysis | GoEmotions, scikit-learn, TensorFlow   |
| Deployment       | Live Server / Python / Node.js         |

---

## How to Run

### Quick Start with Setup Script

Run our automated setup script to download the dataset, install dependencies, and train the emotion model:

```bash
python setup.py
```

### Manual Setup

# Option 1: Using VS Code Live Server 
Open your project folder in VS Code:

1. Install the "Live Server" extension if you haven't already

2. Right-click on your index.html file and select "Open with Live Server"

3. Your browser should automatically open to http://localhost:5500 (or similar port)


# Option 2: Using Python's Built-in Server
Open a terminal/command prompt in your project directory:

1. Run one of these commands depending on your Python version:

Python 3: python -m http.server 8000

Python 2: python -m SimpleHTTPServer 8000

Open your browser to http://localhost:8000


# Option 3: Using Node.js http-server
Install Node.js

1. Install http-server globally: npm install -g http-server

2. In your project directory, run: http-server

Open your browser to http://localhost:8080

## Run the following in your project directory for the final website:

```bash
http-server -o landing.html
```

## Emotion Detection Chatbot

To run the emotion-aware chatbot:

1. Download the GoEmotions dataset:
```bash
python download_dataset.py
```

2. Install the required dependencies:
```bash
pip install -r chatbot/requirements.txt
```

3. Train the emotion detection model:
```bash
python chatbot/train_emotion_model.py
```

4. Start the Streamlit app:
```bash
cd chatbot
streamlit run app.py
```

##  API Key
* To use the OpenRouter integration, generate your key here:  👉 https://openrouter.ai/settings/keys

* Or use this key for testing: c86f97014f5a60d01e85903a5f2a7a7989b1628f.

##  Team Members

**SINDHU.T**
*MADHUSUDHAN.S
*SWAROOP.S
*DIPESH.K

## Credits and Acknowledgements

* **GoEmotions Dataset**: Developed by Google Research, containing 58k Reddit comments with annotations for 27 emotion categories and Neutral.



#
