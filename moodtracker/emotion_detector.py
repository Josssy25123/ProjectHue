from transformers import pipeline

# Load the Hugging Face emotion detection pipeline
emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)

def detect_emotion(text):
    """
    Detects emotion from the provided text.
    Returns a dictionary with emotions and their scores.
    """
    if not text.strip():
        return None

    results = emotion_classifier(text)
    emotions = {res['label']: res['score'] for res in results[0]}
    detected_emotion = max(emotions, key=emotions.get)  # Get the emotion with the highest score
    return {
        "detected_emotion": detected_emotion,
        "scores": emotions
    }