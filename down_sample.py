import os
import cv2

input_dir = 'VisitCardDataset'          # Original image folder
output_dir = 'Downsample-VisitCardDataset'  # Output folder
os.makedirs(output_dir, exist_ok=True)

max_side = 2000  # Only downsample if width or height > 2000

for fname in os.listdir(input_dir):
    if not fname.lower().endswith(('.jpg', '.jpeg', '.png')):
        continue

    fpath = os.path.join(input_dir, fname)
    img = cv2.imread(fpath)
    if img is None:
        print(f"Failed to load {fname}")
        continue

    h, w = img.shape[:2]

    if h > max_side or w > max_side:
        scale = min(max_side / h, max_side / w)
        new_w = int(w * scale)
        new_h = int(h * scale)
        img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
        print(f"Resized {fname} from {w}x{h} → {new_w}x{new_h}")
    else:
        print(f"Kept {fname} unchanged at {w}x{h}")

    out_fpath = os.path.join(output_dir, fname)
    cv2.imwrite(out_fpath, img)

print("\nAll images processed.")
