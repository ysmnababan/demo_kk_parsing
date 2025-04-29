import io
import cv2
import numpy as np
from google.cloud import vision
from PIL import Image

def detect_words_with_positions(image_path):
    client = vision.ImageAnnotatorClient()

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)

    if response.error.message:
        raise Exception(f'Error: {response.error.message}')

    words_with_pos = []
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    text = ''.join([symbol.text for symbol in word.symbols])
                    # bounding box vertices
                    vertices = word.bounding_box.vertices
                    x = sum([v.x for v in vertices]) / 4
                    y = sum([v.y for v in vertices]) / 4
                    words_with_pos.append((text, x, y))
    return words_with_pos

def find_value_by_keyword(words_with_pos, keyword):
    # Find all words joined together to form full text
    all_text = ' '.join([w for w, _, _ in words_with_pos])

    if keyword.lower() not in all_text.lower():
        return None

    # Find keyword position
    for idx, (word, x, y) in enumerate(words_with_pos):
        if keyword.lower() in word.lower():
            # Look for the next words to the right (x > current_x) and close y (same row)
            keyword_x, keyword_y = x, y
            candidates = []
            for w, wx, wy in words_with_pos:
                if wx > keyword_x and abs(wy - keyword_y) < 20:  # tolerance for same line
                    candidates.append((wx, w))
            candidates.sort()  # sort by x position
            value = ' '.join(w for _, w in candidates)
            return value if value else None
    return None

def load_image_as_cv2(image_path):
    pil_image = Image.open(image_path).convert('RGB')
    return np.array(pil_image)

def draw_boxes_on_image(image_path, output_path='./output/output_with_boxes.png'):
    client = vision.ImageAnnotatorClient()
    
    # Load image and send to Google Vision
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)

    if response.error.message:
        raise Exception(response.error.message)

    # Convert image for OpenCV
    image_cv = load_image_as_cv2(image_path)

    # Draw bounding boxes around words
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_text = ''.join([symbol.text for symbol in word.symbols])
                    vertices = [(vertex.x, vertex.y) for vertex in word.bounding_box.vertices]
                    
                    # Draw the bounding box
                    cv2.polylines(image_cv, [np.array(vertices)], isClosed=True, color=(0, 255, 0), thickness=2)
                    
                    # Draw the word text above it
                    x, y = vertices[0]
                    cv2.putText(image_cv, word_text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    # Save the output image
    cv2.imwrite(output_path, cv2.cvtColor(image_cv, cv2.COLOR_RGB2BGR))
    print(f"Saved visualized image to {output_path}")

if __name__ == '__main__':

    image_path = './output/horizontal_part_1.png'
    draw_boxes_on_image(image_path)
    words_with_pos = detect_words_with_positions(image_path)

    # Print all words and their positions
    for word, x, y in words_with_pos:
        print(f"{word} at ({x:.0f}, {y:.0f})")

    keyword = "Alamat"  # You can change this to "Kode Pos" or any other key

    value = find_value_by_keyword(words_with_pos, keyword)
    print(f"Value for '{keyword}': {value}")

    keyword = "Keluarga"  # You can change this to "Kode Pos" or any other key

    value = find_value_by_keyword(words_with_pos, keyword)
    print(f"Value for '{keyword}': {value}")

    keyword = "RW"  # You can change this to "Kode Pos" or any other key

    value = find_value_by_keyword(words_with_pos, keyword)
    print(f"Value for '{keyword}': {value}")

    keyword = "Pos"  # You can change this to "Kode Pos" or any other key

    value = find_value_by_keyword(words_with_pos, keyword)
    print(f"Value for '{keyword}': {value}")