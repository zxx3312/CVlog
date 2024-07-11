import os
import detector3
import dlib
import numpy as np
from matplotlib import pyplot as plt
from skimage.feature import hog
# import more libraries as you need
import cv2
import tqdm

# T1  start _______________________________________________________________________________
# Read in Dataset

# change the dataset path here according to your folder structure


dataset_path = "../20_GeorgiaTechFaces/img_align_celeba/img_align_celeba"
predictor_path = '../shape_predictor_68_face_landmarks.dat/shape_predictor_68_face_landmarks.dat'
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)

X = []
for img_name in tqdm.tqdm(os.listdir(dataset_path), desc='reading images'):
    if img_name.endswith('.jpg'):
        img_path = os.path.join(dataset_path, img_name)
        img = cv2.imread(img_path)
        if img is not None:
            X.append(img)

dataset_path = '../GeorgiaTechFaces/Maskedset_1'
X_masked = []
for img_name in tqdm.tqdm(os.listdir(dataset_path), desc='reading images'):
    if img_name.endswith('.jpg'):
        img_path = os.path.join(dataset_path, img_name)
        img = cv2.imread(img_path)
        if img is not None:
            X_masked.append(img)

X_maskprocessed = []
X_processed = []
for i in tqdm.tqdm(range(len(X)), desc='preprocessing images '):
    temp_X_processed = []
    temp_X_maskprocessed = []
    x_list = X
    x_masklist = X_masked
    temp_img, temp_maskimg = detector3.crop_and_resize_face(x_list[i], x_masklist[i], detector, predictor)

    # append the converted image into temp_X_processed
    # append temp_X_processed into  X_processed
    X_processed.append(temp_img)
    X_maskprocessed.append(temp_maskimg)

# Save the processed images
maskprocessed_dataset_path = '../GeorgiaTechFaces/Maskedcrop_1'
for i, img in enumerate(X_masked):
    img_save_path = os.path.join(maskprocessed_dataset_path, f"{str(i + 1).zfill(5)}.jpg")
    cv2.imwrite(img_save_path, img)

processed_dataset_path = '../GeorgiaTechFaces/Crop_1'
for i, img in enumerate(X_masked):
    img_save_path = os.path.join(processed_dataset_path, f"{str(i + 1).zfill(5)}.jpg")
    cv2.imwrite(img_save_path, img)


