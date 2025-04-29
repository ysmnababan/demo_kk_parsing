import cv2
import TableLinesRemover as tlr
import KKStructure as kk
import TableScanner as ts

structure = kk.KKStructure()
structure.execute("./output/kk_data.json")

# ===========
# image_path = "./output/horizontal_part_3.png"
# img = cv2.imread(image_path)
# lines_remover = tlr.TableLinesRemover(img)
# lines_remover.execute("./output/sliced_lower_table")
# =============

# table_scanner = ts.TableScanner()
# # extracted_text = table_scanner.extract_document_text_from_image("./output/horizontal_part_1.png")
# # Extract the full text and text annotations (bounding boxes) from the image
# extracted_text, text_annotations = table_scanner.extract_document_text_from_image("./output/horizontal_part_1.png")

# # Print the extracted text (optional, for debugging)
# print("Extracted Text:")
# print(extracted_text.text)

# # Reorganize and display the text based on bounding box positions
# reorganized_text = table_scanner.reorganize_text_by_bounding_box(text_annotations)
# print("Reorganized Text:")
# print(reorganized_text)

# # Print the bounding boxes and layout of the extracted text (debugging output)
# table_scanner.print_text_annotations(text_annotations)
# # Define the key you're searching for
# key_to_search = "Provinsi"

# # Get the value corresponding to the provided key using position
# value = table_scanner.get_key_value_using_position(extracted_text, text_annotations, key_to_search)

# print(f"Value for '{key_to_search}': {value}")