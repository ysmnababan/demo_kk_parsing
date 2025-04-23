import cv2
import TableLinesRemover as tlr

image_path = "./output/horizontal_part_3.png"
img = cv2.imread(image_path)
lines_remover = tlr.TableLinesRemover(img)
lines_remover.execute()