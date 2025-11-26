import os
from ultralytics import YOLO
from PIL import Image
model = YOLO('best (5).pt')
image_folder = 'data'  
output_folder = 'results'
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(image_folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        image_path = os.path.join(image_folder, filename)
        results = model(image_path)
        
        # Save image with boxes
        results[0].save(filename=os.path.join(output_folder, filename))
        
        # Save detections to text file
        txt_output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + '.txt')
        with open(txt_output_path, 'w') as f:
            for box in results[0].boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                xywh = box.xywh[0].tolist()
                f.write(f"{cls} {conf:.4f} {' '.join(map(str, xywh))}\n")