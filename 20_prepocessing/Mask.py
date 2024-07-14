import os

import dlib
import numpy as np
from matplotlib import pyplot as plt
from skimage.feature import hog
# import more libraries as you need
import cv2
import tqdm
import preprocessing_utils

dataset_path = "../20_GeorgiaTechFaces/dataset/part_1"
predictor_path = '../shape_predictor_68_face_landmarks.dat/shape_predictor_68_face_landmarks.dat'
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)

# 读取图像编号和人物序号的映射文件
label_mapping_file = "../identity_CelebA.txt"  # 替换为你的映射文件路径
image_labels_dict = {}

with open(label_mapping_file, 'r') as f:
    for line in f:
        img_name, label = line.strip().split()
        image_labels_dict[img_name] = int(label)

X = []
image_numbers = []
count = 0
for img_name in tqdm.tqdm(os.listdir(dataset_path), desc='reading images'):
    if img_name.endswith('.jpg'):
        # count += 1
        # if count % 10 == 0:  # 每隔十个图片读取一张
        img_path = os.path.join(dataset_path, img_name)
        img = cv2.imread(img_path)
        if img is not None:
            X.append(img)
            image_numbers.append(img_name.split('.')[0] + ".jpg")  # 记录图片编号
        # if len(X) >= 20000:  # 达到20000张图片时结束
        #     break
# add the temp_x_list to X

def add_mask(image, landmarks):
    # 使用适当的特征点来绘制口罩
    mask_points = landmarks[1:16]  # 选择适当的面部标志点来绘制口罩
    mask_points = np.concatenate([mask_points, [landmarks[35], landmarks[27], landmarks[31]]])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, [mask_points], (255, 255, 255))
    masked_image = cv2.addWeighted(image, 1, mask, 1, 0)
    return masked_image


X_masked = []
related = []
rotate = []
image_labels = []
for x, img_number in tqdm.tqdm(zip(X, image_numbers), desc='adding masks'):
    dets = detector(x, 1)
    if len(dets) == 0:
        print('no featrues')
    for k, d in enumerate(dets):
        shape = predictor(x, d)
        landmarks = np.array([[p.x, p.y] for p in shape.parts()])
        masked_face = add_mask(x, landmarks)
        rotate_face = preprocessing_utils.random_rotate(x)
        related.append(x)
        rotate.append(rotate_face)
        X_masked.append(masked_face)
    if img_number in image_labels_dict:
        image_labels.append((img_number, image_labels_dict[img_number]))  # 记录图片编号和人物序号
    else:
        image_labels.append((img_number, -1))

Masked_dataset_path = "../20_GeorgiaTechFaces/masked/part_1"
related_dataset_path = "../20_GeorgiaTechFaces/related/part_1"
rotate_dataset_path = "../20_GeorgiaTechFaces/rotate/part_1"

# 确保目录存在，如果不存在则创建
if not os.path.exists(Masked_dataset_path):
    os.makedirs(Masked_dataset_path)
# Save the processed images
for i, img in enumerate(X_masked):
    cv2.imwrite(os.path.join(Masked_dataset_path, f"{str(i + 1).zfill(6)}.jpg"), img)

if not os.path.exists(related_dataset_path):
    os.makedirs(related_dataset_path)
# Save the processed images
for i, img in enumerate(related):
    cv2.imwrite(os.path.join(related_dataset_path, f"{str(i + 1).zfill(6)}.png"), img)

if not os.path.exists(rotate_dataset_path):
    os.makedirs(rotate_dataset_path)
# Save the processed images
for i, img in enumerate(rotate):
    cv2.imwrite(os.path.join(rotate_dataset_path, f"{str(i + 1).zfill(6)}.jpg"), img)

path = '../20_GeorgiaTechFaces'
# 将图片编号和人物序号保存到txt文件中
with open(os.path.join(Masked_dataset_path, "mask_part_1_labels.txt"), 'w') as f:
    for img_number, label in image_labels:
        f.write(f"{img_number} {label}\n")