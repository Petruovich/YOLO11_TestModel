import os
from PIL import Image

def convert_to_yolo(input_dir, output_dir, img_dir):

    os.makedirs(output_dir, exist_ok=True)

    for file_name in os.listdir(input_dir):
        if not file_name.endswith(".txt"):
            continue

        input_path = os.path.join(input_dir, file_name)
        output_path = os.path.join(output_dir, file_name)

        img_name = file_name.replace(".txt", ".jpg")
        img_path = os.path.join(img_dir, img_name)

        if not os.path.exists(img_path):
            print(f"Image not found for annotation: {file_name}")
            continue

        with Image.open(img_path) as img:
            img_width, img_height = img.size

        with open(input_path, "r") as infile, open(output_path, "w") as outfile:
            for line in infile:
                parts = line.strip().split(",")
                if len(parts) < 5:
                    continue

                x_min, y_min, x_max, y_max, class_id = map(float, parts[:5])

                if x_min >= x_max or y_min >= y_max:
                    print(f"Invalid annotation in {file_name}: {line.strip()}")
                    continue

                x_center = (x_min + x_max) / 2.0
                y_center = (y_min + y_max) / 2.0
                width = x_max - x_min
                height = y_max - y_min

                x_center /= img_width
                y_center /= img_height
                width /= img_width
                height /= img_height

                if any(coord < 0 or coord > 1 for coord in [x_center, y_center, width, height]):
                    print(f"Negative or out-of-range values in {file_name}: {line.strip()}")
                    continue

                outfile.write(f"{int(class_id)} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

input_annotations = r"\YOLO_TEST_V1\ValAnnotations\annotations"
output_labels = r"\YOLO_TEST_V1\Val\labels"
images_dir = r"\YOLO_TEST_V1\Val\images"

convert_to_yolo(input_annotations, output_labels, images_dir)

