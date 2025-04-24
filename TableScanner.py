from google.cloud import vision
import io

class TableScanner:
    def detect_single_image(self, image_path):
        client = vision.ImageAnnotatorClient()

        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        # You can also use client.text_detection() for simpler cases
        response = client.document_text_detection(image=image)
        text = response.full_text_annotation.text

        if response.error.message:
            raise Exception(response.error.message)
        
        # Split text by lines and strip leading/trailing whitespace
        lines = [line.strip() for line in text.split('\n') if line.strip()]

        return lines
    
