from google.cloud import vision
import io

class TableScanner:
    def filter_education_lines(self, lines):
        start_idx = None
        for idx, line in enumerate(lines):
            if '(' in line and ')' in line:
                start_idx = idx + 1  # skip the () line itself
                break

        if start_idx is not None:
            return lines[start_idx:]
        else:
            return []  # no valid data found
    
    def detect_single_image(self, image_path):
        client = vision.ImageAnnotatorClient()
        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)

        response = client.document_text_detection(image=image)

        if response.error.message:
            raise Exception(response.error.message)

        # Collect lines with their Y center
        lines = []

        for page in response.full_text_annotation.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    words = []
                    ys = []

                    for word in paragraph.words:
                        text = ''.join([symbol.text for symbol in word.symbols])
                        words.append(text)

                        # Compute Y center
                        vertices = word.bounding_box.vertices
                        y_center = sum(v.y for v in vertices) / 4
                        ys.append(y_center)

                    line_text = ' '.join(words)
                    avg_y = sum(ys) / len(ys) if ys else 0
                    lines.append((avg_y, line_text))

        # Sort by Y position (top to bottom)
        lines.sort(key=lambda x: x[0])

        # Merge lines with similar Y position
        merged_lines = []
        threshold = 10  # tune this threshold if needed
        current_y = None
        current_line = ''

        for y, text in lines:
            if current_y is None:
                current_y = y
                current_line = text
            elif abs(y - current_y) <= threshold:
                current_line += ' ' + text
            else:
                merged_lines.append(current_line.strip())
                current_line = text
                current_y = y

        if current_line:
            merged_lines.append(current_line.strip())

        return self.filter_education_lines(merged_lines)
    
