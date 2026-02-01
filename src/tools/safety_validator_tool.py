
import fasttext
import os

class SafetyValidator:
    def __init__(self, toxicity_threshold=0.5, model_path=None):
        # Load the fastText model for toxicity detection
        if model_path is None:
            model_path = os.path.join(os.path.dirname(__file__), "toxicity_model.bin")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"fastText model not found at {model_path}. Please provide a valid model path.")
        self.model = fasttext.load_model(model_path)
        self.threshold = toxicity_threshold
        # Security: Common prompt injection phrases
        self.injection_keywords = [
            "ignore all previous", "system prompt", "you are now a", 
            "forget your instructions", "jailbreak"
        ]

    def validate(self, text):
        # 1. Check for Toxicity using fastText model
        labels, probabilities = self.model.predict(text)
        # Assuming the model is trained for toxicity detection and label '__label__toxic' is used
        toxic_score = 0.0
        for label, prob in zip(labels, probabilities):
            if label == "__label__toxic":
                toxic_score = prob
                break
        if toxic_score > self.threshold:
            return False, f"Toxicity detected (Score: {toxic_score:.2f})"

        # 2. Check for Prompt Injection
        if any(phrase in text.lower() for phrase in self.injection_keywords):
            return False, "Potential security/injection attempt detected."

        return True, "Valid"

