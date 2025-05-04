import cv2
import numpy as np
import os
import TableLinesRemover as tlr
class ImageClickZoom:
    def order_points_clockwise(self, pts):
        # pts: list of 4 (x, y) points
        rect = np.zeros((4, 2), dtype="float32")

        pts = np.array(pts)

        # sum: top-left has smallest sum, bottom-right has largest
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        # diff: top-right has smallest diff, bottom-left has largest
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        return rect
    
    def __init__(self, image, scale_init=0.5):
        self.image = image
        self.original = image.copy()
        self.scale = scale_init
        self.min_scale = 0.1
        self.max_scale = 3.0

        self.offset = [0, 0]  # For panning
        self.drag_start = None
        self.window_name = "Click 4 Corners - Zoom & Drag (press q to quit)"

        self.clicked_points = []

    def show(self):
        cv2.namedWindow(self.window_name)
        cv2.setMouseCallback(self.window_name, self.mouse_callback)

        while True:
            disp_img = self.get_display_image()
            for pt in self.clicked_points:
                x, y = self.world_to_screen(pt)
                cv2.circle(disp_img, (x, y), 5, (0, 0, 255), -1)

            cv2.imshow(self.window_name, disp_img)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or len(self.clicked_points) == 4:
                break

        cv2.destroyWindow(self.window_name)
        return self.clicked_points

    def get_display_image(self):
        h, w = self.image.shape[:2]
        view = cv2.resize(self.image, (int(w * self.scale), int(h * self.scale)))
        return view

    def world_to_screen(self, pt):
        return (int(pt[0] * self.scale), int(pt[1] * self.scale))

    def screen_to_world(self, x, y):
        return (int(x / self.scale), int(y / self.scale))

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            world_pt = self.screen_to_world(x, y)
            if len(self.clicked_points) < 4:
                self.clicked_points.append(world_pt)
                print(f"Point {len(self.clicked_points)}: {world_pt}")
        elif event == cv2.EVENT_MOUSEWHEEL:
            old_scale = self.scale
            if flags > 0:  # Scroll up
                self.scale *= 1.1
            else:  # Scroll down
                self.scale *= 0.9
            self.scale = max(self.min_scale, min(self.scale, self.max_scale))
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.drag_start = (x, y)
        elif event == cv2.EVENT_MOUSEMOVE and self.drag_start:
            dx = x - self.drag_start[0]
            dy = y - self.drag_start[1]
            self.offset[0] += dx
            self.offset[1] += dy
            self.drag_start = (x, y)
        elif event == cv2.EVENT_RBUTTONUP:
            self.drag_start = None

# === Config ===
TARGET_IMAGE_PATH = './img/kk1.jpeg'
TEMPLATE_IMAGE_PATH = './img/kk_template.png'
OUTPUT_ALIGNED_PATH = './output/aligned_target.png'
CROP_OUTPUT_DIR = 'cropped_cells'

# === Step 1: Load images ===
target = cv2.imread(TARGET_IMAGE_PATH)
template = cv2.imread(TEMPLATE_IMAGE_PATH)

if target is None or template is None:
    raise FileNotFoundError("Check your image paths.")

target = cv2.resize(target, (template.shape[1], template.shape[0]))
h, w = template.shape[:2]

clicker = ImageClickZoom(target, scale_init=0.5)
clicked_points = clicker.show()

if len(clicked_points) != 4:
    print("You must select exactly 4 points.")
    exit()

clicked_points = clicker.order_points_clockwise(clicked_points)

# === Step 3: Warp perspective ===
target_pts = np.array(clicked_points, dtype='float32')
template_pts = np.array([
    [117, 847],
    [6902, 847],
    [6902, 3468],
    [117, 3468]
], dtype='float32')

M = cv2.getPerspectiveTransform(target_pts, template_pts)
aligned_target = cv2.warpPerspective(target, M, (w, h))

# Save aligned image
cv2.imwrite(OUTPUT_ALIGNED_PATH, aligned_target)
print(f"Aligned image saved to: {OUTPUT_ALIGNED_PATH}")

# Reshape to the expected shape (N, 1, 2)
pts = np.array(clicked_points, dtype='float32').reshape(-1, 1, 2)

# Apply the perspective transformation
transformed_points = cv2.perspectiveTransform(pts, M)

# Convert back to simple (x, y) tuples for display
transformed_points = transformed_points.reshape(-1, 2)
print("Transformed points (in aligned image):")
for pt in transformed_points:
    print(f"({pt[0]:.2f}, {pt[1]:.2f})")

y_values = transformed_points[:, 1]
top_y = int(min(y_values))
bottom_y = int(max(y_values))
mid_y = (top_y + bottom_y) // 2

height, width = aligned_target.shape[:2]

# Define horizontal crop regions based on transformed Y coordinates
PADDING = 30
regions = [
    (0, top_y+PADDING),                # Part 1: Above table
    (top_y, mid_y+PADDING),            # Part 2: Top half of table
    (mid_y, bottom_y+PADDING),         # Part 3: Bottom half of table
    (bottom_y, height)         # Part 4: Below table
]

# Crop and save each region
for i, (start_y, end_y) in enumerate(regions, start=1):
    cropped = aligned_target[start_y:end_y, :]
    if i == 2 or i == 3 :
        output_dir= "./output/"
        if i == 2 :
            output_dir+= "sliced_upper_table"
        else :
            output_dir+= "sliced_lower_table"
        lines_remover = tlr.TableLinesRemover(cropped)
        lines_remover.execute(output_dir)
    cv2.imwrite(f"./output/horizontal_part_{i}.png", cropped)