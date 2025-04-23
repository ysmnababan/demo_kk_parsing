import cv2
import numpy as np
import os
class TableLinesRemover:

    def __init__(self, image):
        self.image = image

    def execute(self):
        self.grayscale_image()
        self.store_process_image("0_grayscaled.jpg", self.grey)
        self.threshold_image()
        self.store_process_image("1_thresholded.jpg", self.thresholded_image)
        self.invert_image()
        self.store_process_image("2_inverted.jpg", self.inverted_image)
        self.erode_vertical_lines()
        self.store_process_image("3_erode_vertical_lines.jpg", self.vertical_lines_eroded_image)
        self.erode_horizontal_lines()
        self.store_process_image("4_erode_horizontal_lines.jpg", self.horizontal_lines_eroded_image)

        self.crop_table()
        # self.combine_eroded_images()
        # self.store_process_image("5_combined_eroded_images.jpg", self.combined_image)
        # self.dilate_combined_image_to_make_lines_thicker()
        # self.store_process_image("6_dilated_combined_image.jpg", self.combined_image_dilated)
        # self.subtract_combined_and_dilated_image_from_original_image()
        # self.store_process_image("7_image_without_lines.jpg", self.image_without_lines)
        # self.remove_noise_with_erode_and_dilate()
        # self.store_process_image("8_image_without_lines_noise_removed.jpg", self.image_without_lines_noise_removed)
        # return self.image_without_lines_noise_removed

    def grayscale_image(self):
        self.grey = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    def threshold_image(self):
        self.thresholded_image = cv2.threshold(self.grey, 127, 255, cv2.THRESH_BINARY)[1]

    def invert_image(self):
        self.inverted_image = cv2.bitwise_not(self.thresholded_image)

    def erode_vertical_lines(self):
        hor = np.array([[1,1,1,1,1,1,1,1,1,1]])
        self.vertical_lines_eroded_image = cv2.erode(self.inverted_image, hor, iterations=10)
        self.vertical_lines_eroded_image = cv2.dilate(self.vertical_lines_eroded_image, hor, iterations=10)

    def erode_horizontal_lines(self):
        ver = np.ones((11, 1), dtype=np.uint8) 
        self.horizontal_lines_eroded_image = cv2.erode(self.inverted_image, ver, iterations=10)
        self.horizontal_lines_eroded_image = cv2.dilate(self.horizontal_lines_eroded_image, ver, iterations=10)

    def combine_eroded_images(self):
        self.combined_image = cv2.add(self.vertical_lines_eroded_image, self.horizontal_lines_eroded_image)

    def dilate_combined_image_to_make_lines_thicker(self):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        self.combined_image_dilated = cv2.dilate(self.combined_image, kernel, iterations=5)

    def subtract_combined_and_dilated_image_from_original_image(self):
        self.image_without_lines = cv2.subtract(self.inverted_image, self.combined_image_dilated)

    def remove_noise_with_erode_and_dilate(self):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        self.image_without_lines_noise_removed = cv2.erode(self.image_without_lines, kernel, iterations=1)
        self.image_without_lines_noise_removed = cv2.dilate(self.image_without_lines_noise_removed, kernel, iterations=1)

    def store_process_image(self, file_name, image):
        path = "./output/process_images/table_lines_remover/" + file_name
        cv2.imwrite(path, image)

    def group_close_positions(self, positions, min_dist=15):
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
    
    def crop_table(self):
        line_img = self.horizontal_lines_eroded_image
        # Find vertical lines as non-zero columns
        cols_sum = np.sum(line_img > 0, axis=0)  # Sum vertically to find white lines
        threshold = line_img.shape[0] * 0.5  # Adjust: 50% of image height

        # Get the x-coordinates of white vertical lines
        line_positions = np.where(cols_sum > threshold)[0]
        grouped_lines = self.group_close_positions(line_positions, min_dist=15)

        print(f"Detected {len(grouped_lines)} column dividers: {grouped_lines}")

        if len(grouped_lines) > 1:
            grouped_lines = grouped_lines[1:]
        # Load the aligned original image
        aligned_img = self.image

        # Crop between each pair of dividers
        output_dir = "output/process_images/cropped_columns"
        os.makedirs(output_dir, exist_ok=True)

        for i in range(len(grouped_lines) - 1):
            x_start = grouped_lines[i]
            x_end = grouped_lines[i + 1]
            column_crop = aligned_img[:, x_start:x_end]
            cv2.imwrite(f"{output_dir}/column_{i+1}.png", column_crop)

        print(f"Cropped {len(grouped_lines) - 1} columns.")