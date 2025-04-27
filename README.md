# MindHue

MindHue is an AI-powered mental health web application that helps users reflect on their emotions, track mood trends, and recommend uplifting music and podcasts based on real-time mood detection.

## Demo!

<div style="position: relative; padding-bottom: 56.25%; height: 0;"><iframe src="https://www.loom.com/embed/1a1fe613503d4e978504fd330be8f769?sid=77b7e6e5-91b3-41ae-9217-047d797145f6" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

Click the link above to watch the full demo on Loom.

---

## Poster!

[cosc490 SFP.pptx](https://github.com/user-attachments/files/19927216/cosc490.SFP.pptx)

## Setup Instructions

1. **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/MindHue.git
    cd MindHue
    ```

2. **Create a Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # MacOS/Linux
    venv\Scripts\activate     # Windows
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure Environment Variables**
    - Copy `.env.example` ➔ `.env`
    - Fill in your Django secret key and Spotify API credentials.

5. **Run the Server**
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```
---

## Features

- Chatbot-style emotion journaling
- Real-time AI emotion detection
- Mood trend visualization (Chart.js)
- Spotify music and podcast recommendations based on mood
- Guest mode and user authentication
- Responsive, mobile-friendly UI
- Secure environment variable management

---

## References

1. Hugging Face - DistilRoBERTa emotion model
2. Spotify Web API Documentation
3. Django Software Foundation. (2024). Django (Version 5.2). 
4. Hugging Face Inc. (2024). Transformers Library

---


