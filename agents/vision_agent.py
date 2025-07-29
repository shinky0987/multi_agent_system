from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

class VisionAgent:
    def __init__(self):
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

    def analyze_image(self, image_path):
        image = Image.open(image_path).convert('RGB')
        inputs = self.processor(image, return_tensors="pt")
        out = self.model.generate(**inputs)
        caption = self.processor.decode(out[0], skip_special_tokens=True)
        return caption
