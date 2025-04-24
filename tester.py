import cv2
import TableLinesRemover as tlr
import KKStructure as kk

# structure = kk.KKStructure()
# structure.execute("./output/kk_data.json")
image_path = "./output/horizontal_part_3.png"
img = cv2.imread(image_path)
lines_remover = tlr.TableLinesRemover(img)
lines_remover.execute("./output/sliced_lower_table")



