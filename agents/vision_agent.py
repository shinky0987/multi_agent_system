from PIL import Image
from transformers import BlipProcessor, BlipForQuestionAnswering

class VisionAgent:
    def __init__(self):
        # Load the VQA model and processor
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
        self.model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base")

    def answer_question(self, image_path: str, question: str) -> str:
        """Answers a specific question about the image using a VQA model."""
        try:
            raw_image = Image.open(image_path).convert('RGB')
            
            # Process the image and question
            inputs = self.processor(raw_image, question, return_tensors="pt")
            
            # Generate an answer
            out = self.model.generate(**inputs)
            answer = self.processor.decode(out[0], skip_special_tokens=True)
            
            return answer
        except Exception as e:
            return f"[VisionAgent] Error processing image: {e}"
