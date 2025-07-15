import json
from collections import defaultdict

# Load your OCR result JSON
with open("ocr_result.json", "r", encoding='utf-8') as f:
    data = json.load(f)

# Output dictionary grouped by source_image
grouped = defaultdict(list)

# Convert structure
for item in data:
    entry = {
        "transcription": item["text"],
        "points": item["box"],
        "difficult": False
    }
    grouped[item["source_image"]].append(entry)

# Write in PPOCRLabel format
with open("ppocr_label.txt", "w", encoding='utf-8') as f:
    for image_path, annotations in grouped.items():
        line = f"VisitCardDataset/images/{image_path}\t{json.dumps(annotations, ensure_ascii=False)}\n"
        f.write(line)

print("✅ Converted to 'ppocr_label.txt' for PPOCRLabel.")
