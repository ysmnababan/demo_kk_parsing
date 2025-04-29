import io
from google.cloud import vision

def get_words_with_positions(image_path):
    client = vision.ImageAnnotatorClient()

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)
    if response.error.message:
        raise Exception(response.error.message)

    words = []
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_text = ''.join([symbol.text for symbol in word.symbols])
                    bounding_box = word.bounding_box
                    # Use average of y for the word position
                    avg_y = sum(vertex.y for vertex in bounding_box.vertices) / 4
                    avg_x = sum(vertex.x for vertex in bounding_box.vertices) / 4
                    words.append((word_text, avg_x, avg_y))
    return words

def group_words_into_lines(words, y_threshold=20):
    # First, sort by y
    words.sort(key=lambda w: w[2])

    lines = []
    current_line = []
    last_y = None

    for word, x, y in words:
        if last_y is None:
            current_line.append((word, x))
            last_y = y
        elif abs(y - last_y) <= y_threshold:
            current_line.append((word, x))
            last_y = (last_y + y) / 2  # smooth the y a bit
        else:
            lines.append(current_line)
            current_line = [(word, x)]
            last_y = y
    if current_line:
        lines.append(current_line)
    return lines

def print_reconstructed_text(lines, space_threshold=100):
    for line in lines:
        # Sort words left to right
        line.sort(key=lambda w: w[1])

        output_line = ''
        last_x = None
        for word, x in line:
            if last_x is None:
                output_line += word
                last_x = x
            else:
                gap = x - last_x
                num_spaces = int(gap / space_threshold)
                if num_spaces > 0:
                    output_line += '_' * num_spaces
                else:
                    output_line += '_'
                output_line += word
                last_x = x + len(word) * 10  # Estimate next position
        print(output_line)

def main():
    image_path = './output/horizontal_part_1.png'
    words = get_words_with_positions(image_path)
    lines = group_words_into_lines(words)
    print_reconstructed_text(lines)

if __name__ == "__main__":
    main()