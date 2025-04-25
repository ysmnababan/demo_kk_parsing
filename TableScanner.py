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

        annotations = response.text_annotations

        if not annotations:
            return []

        blocks = []
        for annotation in annotations[1:]:
            text = annotation.description
            vertices = annotation.bounding_poly.vertices
            top = min(vertex.y for vertex in vertices)
            left = min(vertex.x for vertex in vertices)
            blocks.append({'text': text, 'top': top, 'left': left})

        # Sort by top first
        blocks.sort(key=lambda b: (b['top'], b['left']))

        # Group by y-axis (same line if y is close enough)
        lines = []
        current_line = []
        last_top = None
        threshold = 10  # pixel threshold for grouping in same row

        for block in blocks:
            if last_top is None:
                current_line.append(block)
                last_top = block['top']
                continue

            if abs(block['top'] - last_top) <= threshold:
                current_line.append(block)
            else:
                # Sort current line left to right
                current_line.sort(key=lambda b: b['left'])
                line_text = ' '.join(b['text'] for b in current_line)
                lines.append(line_text)

                # Start new line
                current_line = [block]
                last_top = block['top']

        # Add the last line
        if current_line:
            current_line.sort(key=lambda b: b['left'])
            line_text = ' '.join(b['text'] for b in current_line)
            lines.append(line_text)

        # Filter header until the '()' symbol found

        return self.filter_education_lines(lines)
    
