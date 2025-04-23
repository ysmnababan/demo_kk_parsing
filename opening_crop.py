import cv2
import numpy as np
import os
def group_close_positions(positions, min_dist=15):
    grouped = []
    current_group = []

    for x in positions:
        if not current_group:
            current_group.append(x)
        elif x - current_group[-1] <= min_dist:
            current_group.append(x)
        else:
            # Average the group as single point
            avg_x = int(np.mean(current_group))
            grouped.append(avg_x)
            current_group = [x]

    # Don't forget the last group
    if current_group:
        avg_x = int(np.mean(current_group))
        grouped.append(avg_x)

    return grouped

# Load the vertical lines image (binary mask)
line_img = cv2.imread("./output/process_images/table_lines_remover/4_erode_horizontal_lines.jpg", cv2.IMREAD_GRAYSCALE)

# Find vertical lines as non-zero columns
cols_sum = np.sum(line_img > 0, axis=0)  # Sum vertically to find white lines
threshold = line_img.shape[0] * 0.5  # Adjust: 50% of image height

# Get the x-coordinates of white vertical lines
line_positions = np.where(cols_sum > threshold)[0]
grouped_lines = group_close_positions(line_positions, min_dist=15)

print(f"Detected {len(grouped_lines)} column dividers: {grouped_lines}")

if len(grouped_lines) > 1:
    grouped_lines = grouped_lines[1:]
# Load the aligned original image
aligned_img = cv2.imread("./output/horizontal_part_2.png")

# Crop between each pair of dividers
output_dir = "cropped_columns"
os.makedirs(output_dir, exist_ok=True)

for i in range(len(grouped_lines) - 1):
    x_start = grouped_lines[i]
    x_end = grouped_lines[i + 1]
    column_crop = aligned_img[:, x_start:x_end]
    cv2.imwrite(f"{output_dir}/column_{i+1}.png", column_crop)

print(f"Cropped {len(grouped_lines) - 1} columns.")