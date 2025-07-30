from transformers import pipeline
import re

class TextModerationAgent:
    def __init__(self):
        # Use a zero-shot classification model to detect intent
        self.classifier = pipeline(
            "zero-shot-classification", 
            model="facebook/bart-large-mnli"
        )
        # Define a comprehensive set of harmful labels
        self.harmful_labels = {
            "system file deletion attempt",
            "malicious command execution", 
            "credit card information request",
            "personal data harvesting",
            "password or credential theft",
            "financial information request",
            "system manipulation attempt",
            "unauthorized access attempt",
            "hate speech", 
            "toxic language",
            "self-harm instruction",
            "illegal activity instruction",
            "privacy violation attempt",
            "social engineering attack"
        }
        # All possible labels for the classifier
        self.candidate_labels = list(self.harmful_labels) + ["safe user query"]
        
        # Define regex patterns for common malicious patterns
        self.malicious_patterns = [
            r'\b(delete|remove|rm)\s+.*\b(system|windows|program files|boot|registry)\b',
            r'\bcredit\s*card\s*(number|details|info|data)\b',
            r'\b(password|passwd|credentials|login)\s*(for|of|to)\b',
            r'\bformat\s+[c-z]:?\b',
            r'\bdel\s+.*\.(exe|dll|sys|bat|cmd)\b',
            r'\b(social\s*security|ssn|bank\s*account)\s*(number|details)\b',
            r'\b(hack|exploit|breach|penetrate)\s+.*\b(system|network|database)\b',
            r'\bshutdown\s*/[srf]\b',
            r'\breg\s+delete\b',
            r'\bnet\s+user\s+.*\s*/delete\b',
            r'\b(give|tell|provide|share)\s+(me|us)?\s*(your|the)?\s*(credit\s*card|password|ssn|social\s*security)\b',
            r'\bwipe\s+(hard\s*drive|disk|system)\b',
            r'\b(destroy|corrupt|damage)\s+(files|data|system)\b',
            r'\binstall\s+(malware|virus|trojan|keylogger)\b',
            r'\baccess\s+(private|confidential|restricted)\s+(files|data|information)\b'
        ]

    def check_regex_patterns(self, text: str) -> (bool, str):
        """
        Check text against known malicious regex patterns.
        Returns (is_malicious, reason)
        """
        text_lower = text.lower()
        for pattern in self.malicious_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return True, f"Matched malicious pattern: {pattern}"
        return False, "No malicious patterns detected"

    def get_intent(self, text: str) -> (str, float):
        """
        Classifies text to determine its intent and returns the label and score.
        """
        result = self.classifier(text, self.candidate_labels, multi_label=False)
        top_label = result['labels'][0]
        top_score = result['scores'][0]
        return top_label, top_score

    def is_malicious(self, text: str) -> (bool, str):
        """
        Determines if the text is malicious.
        Returns (is_malicious, reason)
        """
        # First check regex patterns for quick detection
        is_pattern_match, pattern_reason = self.check_regex_patterns(text)
        if is_pattern_match:
            return True, f"Pattern detection: {pattern_reason}"
        
        # Then use AI classification
        top_label, top_score = self.get_intent(text)
        
        # Lower the threshold for better detection and check if it's a harmful label
        if top_label in self.harmful_labels and top_score > 0.5:
            return True, f"AI classification: {top_label} (confidence: {top_score:.2f})"
        
        return False, "Text appears safe"

    def is_safe(self, text: str) -> bool:
        """
        Determines if the text is safe to process.
        Returns True if the text is safe, False otherwise.
        """
        is_malicious, _ = self.is_malicious(text)
        return not is_malicious
