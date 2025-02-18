import cv2
import numpy as np
import os
from glob import glob


# 設定資料夾
image_folder = "./KolektorSDD"
output_dataset_path = "Datasets"  # YOLO 資料集輸出資料夾

# 建立 YOLO 資料夾結構
os.makedirs(f"{output_dataset_path}/images/train", exist_ok=True)
os.makedirs(f"{output_dataset_path}/images/val", exist_ok=True)
os.makedirs(f"{output_dataset_path}/labels/train", exist_ok=True)
os.makedirs(f"{output_dataset_path}/labels/val", exist_ok=True)


image_folders = [f'{image_folder}/{i}' for i in os.listdir(image_folder)]

total = 0
for img_path in image_folders: total += len(os.listdir(img_path))

# 設定訓練/驗證比例
split_ratio = 0.8  # 80% 訓練，20% 驗證
num_train = int(total//2) * split_ratio

image_number = 0 # 影像編號

for img_path in image_folders:
    for img in os.listdir(img_path):
        # 決定要放進 train 或 val
        dataset_type = "train" if image_number < num_train else "val"
        if ".bmp" in os.path.basename(img):
            filename = os.path.basename(img).replace("_label.bmp", "")
            # 複製影像到 YOLO 資料夾
            os.rename(f"{img_path}/{filename}.jpg", f"{output_dataset_path}/images/{dataset_type}/{image_number:03}.jpg") 

            # 讀取 BMP 標註影像
            if os.path.exists(f"{img_path}/{img}"):
                label_img = cv2.imread(f"{img_path}/{img}", cv2.IMREAD_GRAYSCALE)
                h, w = label_img.shape
                
                # 找到輪廓 (白色區域)
                contours, _ = cv2.findContours(label_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                yolo_annotations = []
                for contour in contours:
                    # 獲取輪廓的 x, y 座標並轉換為 YOLO 格式 (0~1)
                    normalized_contour = [(point[0][0] / w, point[0][1] / h) for point in contour]
                    flattened_contour = [coord for point in normalized_contour for coord in point]
                    
                    # 如果輪廓點數大於 3，則儲存
                    if len(flattened_contour) >= 6:
                        yolo_annotations.append(f"0 " + " ".join(map(str, flattened_contour)))

                # 儲存標註為 YOLO 格式
                with open(f"{output_dataset_path}/labels/{dataset_type}/{image_number:03}.txt", "w") as f:
                    f.write("\n".join(yolo_annotations))
            else:
                # 沒有瑕疵時，寫入空白標註檔
                open(f"{output_dataset_path}/labels/{dataset_type}/{image_number:03}.txt", "w").close()
            image_number += 1