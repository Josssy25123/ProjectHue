# MindHue

MindHue is an AI-powered mental health web application that helps users reflect on their emotions, track mood trends, and recommend uplifting music and podcasts based on real-time mood detection.

---

## Poster!

[cosc490 SFP.pptx](https://github.com/user-attachments/files/19927216/cosc490.SFP.pptx)

## Setup Instructions (Windows)

1. **Clone the repository**
    ```bash
    git clone https://github.com/josssy25123/MindHue.git
    cd MindHue
    ```

2. **Create a Virtual Environment**
    ```bash
    python -m venv venv
    venv\Scripts\activate    
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


