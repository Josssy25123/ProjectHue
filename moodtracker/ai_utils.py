from transformers import pipeline

emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)

def detect_emotions(text):
    """
    Detect emotions from text and return top emotion.
    """
    if not text.strip():
        return "Neutral" # if no text is provided
    
    results = emotion_classifier(text)

    #find highest confidence emotion
    top_emotion = max(results[0], key=lambda x: x['score'])

    return top_emotion['label']