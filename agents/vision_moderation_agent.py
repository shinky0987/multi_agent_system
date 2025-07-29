from transformers import pipeline

class VisionModerationAgent:
    def __init__(self):
        self.moderation_pipeline = pipeline(
            "image-classification", 
            model="Falconsai/nsfw_image_detection"
        )

    def moderate_image(self, image_path):
        """Analyzes an image for NSFW content and returns the label."""
        results = self.moderation_pipeline(image_path)
        # The model returns a list of dictionaries, we get the highest score
        top_result = max(results, key=lambda x: x['score'])
        return top_result['label']
