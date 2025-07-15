import os
from PIL import Image
import pillow_heif

folder_path = 'VisitCardDataset'

for fname in os.listdir(folder_path):
    if fname.lower().endswith('.heic'):
        heic_path = os.path.join(folder_path, fname)
        jpg_path = os.path.splitext(heic_path)[0] + '.jpg'
        heif_file = pillow_heif.read_heif(heic_path)
        image = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw"   
        )
        image.save(jpg_path, "JPEG")
        os.remove(heic_path)

