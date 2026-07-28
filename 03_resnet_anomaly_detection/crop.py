import os
import cv2
from ultralytics import YOLO

model_path = "/home/sht/runs/segment/train-2/weights/best.pt"
model = YOLO(model_path)

input_root = "/home/sht/cube_raw_dataset"
output_root = "/home/sht/cube_crop_dataset"

# 예시 폴더 구조:
# /home/sht/cube_raw_dataset/train/good
# /home/sht/cube_raw_dataset/test/good
# /home/sht/cube_raw_dataset/test/bad

folders = [
    ("train/good", "train/good"),
    ("test/good", "test/good"),
    ("test/bad", "test/bad"),
]

PAD = 30
CONF_THRES = 0.4

def crop_cube_image(image_path, save_dir):
    os.makedirs(save_dir, exist_ok=True)

    image = cv2.imread(image_path)
    if image is None:
        print(f"이미지 읽기 실패: {image_path}")
        return

    h, w = image.shape[:2]
    results = model(image, conf=CONF_THRES)

    if len(results) == 0 or results[0].boxes is None or len(results[0].boxes) == 0:
        print(f"cube 미검출: {image_path}")
        return

    boxes = results[0].boxes
    confs = boxes.conf.cpu().numpy()
    best_idx = confs.argmax()

    x1, y1, x2, y2 = boxes.xyxy[best_idx].cpu().numpy().astype(int)

    box_w = x2 - x1
    box_h = y2 - y1
    pad = int(max(box_w, box_h) * 0.2)  # bbox 크기의 20% 여백

    x1 = max(0, x1 - pad)
    y1 = max(0, y1 - pad)
    x2 = min(w, x2 + pad)
    y2 = min(h, y2 + pad)

    crop = image[y1:y2, x1:x2]

    if crop.size == 0:
        print(f"crop 실패: {image_path}")
        return

    crop_224 = cv2.resize(crop, (224, 224), interpolation=cv2.INTER_AREA)

    filename = os.path.basename(image_path)
    save_path = os.path.join(save_dir, filename)

    cv2.imwrite(save_path, crop_224)
    print(f"saved: {save_path}")