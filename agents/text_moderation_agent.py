from transformers import pipeline

class TextModerationAgent:
    def __init__(self):
        # Use a zero-shot classification model to detect intent
        self.classifier = pipeline(
            "zero-shot-classification", 
            model="facebook/bart-large-mnli"
        )
        # Define a set of harmful labels for comprehensive moderation
        self.harmful_labels = {
            "malicious command attempt", 
            "hate speech", 
            "toxic language",
            "self-harm instruction"
        }
        # All possible labels for the classifier
        self.candidate_labels = list(self.harmful_labels) + ["safe user query"]

    def get_intent(self, text: str) -> (str, float):
        """
        Classifies text to determine its intent and returns the label and score.
        """
        result = self.classifier(text, self.candidate_labels, multi_label=False)
        top_label = result['labels'][0]
        top_score = result['scores'][0]
        return top_label, top_score

    def is_safe(self, text: str) -> bool:
        """
        Determines if the text is safe to process.
        Returns True if the text is safe, False otherwise.
        """
        top_label, top_score = self.get_intent(text)
        
        # If the top-scoring label is harmful and exceeds our confidence threshold, it's not safe.
        if top_label in self.harmful_labels and top_score > 0.7:
            return False # It is not safe
        
        return True # It is safe
