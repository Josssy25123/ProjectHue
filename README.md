# MindHue: AI-Powered Emotion Tracking and Wellness Recommendations

Abstract:

MindHue is a web application that allows users to record their feelings through natural text input.
Using Hugging Face emotion detection and Spotify API integrations, the app suggests mood-based activities,
music, and podcasts to promote mental wellness. It supports both registered users and anonymous guests.

Introduction:

Emotional awareness is critical for mental health management.
MindHue leverages state-of-the-art Natural Language Processing (NLP) models to detect a user's emotional state from free-form text input.
It then dynamically recommends supportive media such as songs and podcasts aligned with the user's detected mood.
In addition, MindHue visualizes emotional trends over time with interactive graphs to help users monitor their well-being patterns.

Features:

AI-powered emotion detection (Hugging Face Transformers)
Mood-specific Spotify song and podcast recommendations
Guest and registered user support
Interactive mood trend chart (Chart.js)
Chatbot-style conversational UI
Automatic Spotify token refreshing to ensure seamless recommendations
Privacy-first: minimal data storage for guest users

System Requirements:

Python 3.9 or higher (Tested on Python 3.12)
Node.js (optional, if you modify frontend JavaScript libraries)

Python packages:

See requirements.txt

Setup Instructions:

1. Clone the Repository
2. Create and Activate Virtual Environment
3. Install Requirements
4. Configure Environment Variables

Running Instructions:

1. Apply Database Migrations
2. Run the development server

References:

[1] Hugging Face Transformers Library. Available at: https://huggingface.co/transformers/

[2] Spotify Web API Documentation. Available at: https://developer.spotify.com/documentation/web-api/

[3] Django Documentation. Available at: https://docs.djangoproject.com/en/stable/

[4] Chart.js - Simple yet flexible JavaScript charting. Available at: https://www.chartjs.org/

[5] Spotipy: A lightweight Python library for the Spotify Web API. Available at: https://spotipy.readthedocs.io/en/2.22.1/

[6] Python Decouple. Available at: https://pypi.org/project/python-decouple/

[7] Python Dotenv. Available at: https://pypi.org/project/python-dotenv/

[8] Mathfilters for Django templates. Available at: https://pypi.org/project/django-mathfilters/


NOTES:

The environment automatically refreshes the Spotify access token when needed.

Anonymous users are assigned a cookie to track their mood inputs privately.

The project structure follows Django best practices, separating templates, static files, and environment secrets.


Project Poster:

[cosc490 SFP.pptx](https://github.com/user-attachments/files/19927053/cosc490.SFP.pptx)

Project Demo:

"https://www.loom.com/embed/1a1fe613503d4e978504fd330be8f769?sid=8754bd4e-fd97-470c-8562-7069605204ea"
