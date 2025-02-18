# KolektorSDD_Yolov8_Datasets

## Things to note
When using this dataset, please check the data.yaml file within the Datasets directory. Ensure that the path specified after path: corresponds to the actual location of your dataset.

Importance: This is crucial for the model to correctly locate and utilize your data.
Specific instructions: If the path is incorrect, please modify it accordingly and save the data.yaml file.
Clarification: The path can be either an absolute path (e.g., /home/user/datasets/my_dataset) or a relative path (e.g., ../datasets/my_dataset).


data.yaml
path: Datasets <-- If Can't Work, Try to use the Physical path
train: images/train
val: images/val

nc: 1  # 類別數量
names: ["defect"]  # 類別名稱
task: segment  # 設定為 "segment" 來做實例分割
