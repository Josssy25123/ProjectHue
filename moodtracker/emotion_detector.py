from transformers import pipeline

# Load the Hugging Face emotion detection pipeline
emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=1)

def detect_emotion(text):
    result = emotion_classifier(text)
    return {"detected_emotion": result[0][0]['label'].lower(), "scores": result[0]}