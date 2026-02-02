from detoxify import Detoxify 
from transformers import logging as transformers_logging
transformers_logging.set_verbosity_error()

class SafetyValidator:
    def __init__(self, toxicity_threshold=0.5):

        # Load the toxicity model once (it takes a moment)
        self.model = Detoxify('original-small')
        self.threshold = toxicity_threshold
        
        # Security: Common prompt injection phrases
        self.injection_keywords = [
            "ignore all previous", "system prompt", "you are now a", 
            "forget your instructions", "jailbreak"
        ]              

    def validate(self, text):
        # 1. Check for Toxicity
        results = self.model.predict(text)
        max_toxic_score = max(results.values())
        if max_toxic_score > self.threshold:
            return False, f"Toxicity detected (Score: {max_toxic_score:.2f})"

        # 2. Check for Prompt Injection
        if any(phrase in text.lower() for phrase in self.injection_keywords):
            return False, "Potential security/injection attempt detected."

        return True, "Valid"

