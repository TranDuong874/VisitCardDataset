import os
import json
import cv2
from PIL import Image
import numpy as np

# Input and output paths
label_file = 'dataset/Label.txt'
output_dir = 'paddle_ocr_train_part2'
image_output_dir = os.path.join(output_dir, 'images')
label_output_path = os.path.join(output_dir, 'labels.txt')

# Ensure output directories exist
os.makedirs(image_output_dir, exist_ok=True)

# Read Label.txt and process each line
with open(label_file, 'r', encoding='utf-8') as f_in, open(label_output_path, 'w', encoding='utf-8') as f_out:
    for line in f_in:
        if not line.strip():
            continue
        try:
            img_path, annots = line.strip().split('\t', 1)
            img = cv2.imread(img_path)
            if img is None:
                print(f"Could not read image: {img_path}")
                continue

            data = json.loads(annots)
            for idx, item in enumerate(data):
                text = item.get('transcription', '').strip()
                points = item.get('points', [])

                if len(points) != 4 or text == '':
                    continue

                # Prepare bounding box and crop
                pts = np.array(points, dtype=np.float32)
                rect = cv2.boundingRect(pts)
                x, y, w, h = rect
                cropped = img[y:y+h, x:x+w]

                # Save cropped image
                crop_filename = f"{os.path.splitext(os.path.basename(img_path))[0]}_{idx}.jpg"
                crop_rel_path = f"images/{crop_filename}"
                crop_full_path = os.path.join(image_output_dir, crop_filename)
                cv2.imwrite(crop_full_path, cropped)

                # Write to labels.txt in PaddleOCR format
                f_out.write(f"/{crop_rel_path}\t{text}\n")

        except Exception as e:
            print(f"Error processing line: {line}\n{e}")
